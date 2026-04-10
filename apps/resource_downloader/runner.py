"""
runner.py — CLI interface for the Resource Downloader Engine.

A complete argparse-based command line tool for downloading media.

Commands:
    download    Download media using a named pipeline
    list        List all available pipelines
    search      Find the best pipeline for a keyword query

Usage:
    python -m apps.resource_downloader.runner download --pipeline pexels_image --search "cyberpunk city" --count 40
    python -m apps.resource_downloader.runner list
    python -m apps.resource_downloader.runner list --media image
    python -m apps.resource_downloader.runner search --query "youtube music download mp3"

"""

import argparse
import sys
from pathlib import Path

__ROOT__ = Path(__file__).resolve().absolute().parents[2]
sys.path.insert(0, str(__ROOT__))

from core.styling import (
    BOLD, RESET, SUCCESS, WARNING, ERROR, INFO, DEBUG as DEBUG_STYLE,
    apply_style, Palette, Fore, Back, Style,
)

from apps.resource_downloader.engine import ResourceDownloaderEngine
from apps.resource_downloader.pipelines.register import (
    PIPELINE_REGISTRY,
    discover_pipeline,
    get_pipeline_by_keywords,
    get_pipelines_names,
)


# =========================================================
# CLI COMMANDS
# =========================================================

def cmd_download(args):
    """Execute a download using the engine."""
    engine = ResourceDownloaderEngine(
        max_workers=args.workers,
        debug=args.debug,
    )
    result = engine.download(
        pipeline_name=args.pipeline,
        search_term=args.search,
        item_count=args.count,
        output_dir=args.output,
        safe_search=args.safe_search,
    )
    if result:
        print(f"\n{SUCCESS}✅ Output: {result}{RESET}")
    else:
        print(f"\n{ERROR}❌ Download returned no result.{RESET}")
        sys.exit(1)


def cmd_list(args):
    """List all registered pipelines, optionally filtered by media type."""
    discover_pipeline()

    # Header
    print(f"\n{apply_style('  REGISTERED PIPELINES  ', BOLD, Back.BRIGHT_BLACK, Fore.WHITE)}")
    print(f"{'=' * 80}\n")

    # Column headers
    print(
        f"  {apply_style('Name', BOLD):<30}"
        f"{apply_style('Media', BOLD):<12}"
        f"{apply_style('Rate Limit', BOLD):<16}"
        f"{apply_style('Description', BOLD)}"
    )
    print(f"  {'=' * 76}")

    filtered = PIPELINE_REGISTRY
    if args.media:
        filtered = {
            k: v for k, v in PIPELINE_REGISTRY.items()
            if v.get("media_type") == args.media
        }

    if not filtered:
        print(f"  {WARNING}No pipelines found for media type '{args.media}'{RESET}")
        return

    for name, data in sorted(filtered.items()):
        media = data.get("media_type", "?")
        rate = data.get("api_calls_per_hour")
        rate_str = f"{rate}/hr" if rate else "unlimited"
        desc = data.get("description", "")[:40]

        # Color code by media type
        media_color = {
            "image": Palette.LIME,
            "video": Palette.GOLD,
            "music": Palette.TEAL,
            "gifs": Palette.ROSE,
        }.get(media, "")

        print(
            f"  {Palette.GOLD}{name:<28}{RESET}"
            f"{media_color}{media:<12}{RESET}"
            f"{rate_str:<16}"
            f"{Style.DIM}{desc}{RESET}"
        )

    print(f"\n  {Style.DIM}Total: {len(filtered)} pipeline(s){RESET}\n")


def cmd_search(args):
    """Search for the best pipeline matching a keyword query."""
    discover_pipeline()

    results = get_pipeline_by_keywords(
        args.query,
        strategy=args.strategy,
        fuzzy_threshold=args.threshold,
    )

    if not results:
        print(f"\n{WARNING}No matching pipelines for '{args.query}'.{RESET}")
        print(f"{INFO}Try: --strategy fuzzy  for typo-tolerant search{RESET}\n")
        return

    print(f"\n{apply_style('  PIPELINE SEARCH RESULTS  ', BOLD, Back.BRIGHT_BLACK, Fore.WHITE)}")
    print(f"{'=' * 60}\n")
    print(f"  {apply_style('Pipeline', BOLD):<30}{apply_style('Confidence', BOLD)}")
    print(f"  {'=' * 50}")

    for name, score in results.items():
        bar_len = int(score * 30)
        bar = "#" * bar_len + "." * (30 - bar_len)
        color = Palette.LIME if score >= 0.5 else (Palette.GOLD if score >= 0.2 else Palette.CRIMSON)
        print(f"  {Palette.GOLD}{name:<28}{RESET}{color}{bar} {score:.0%}{RESET}")

    best = next(iter(results))
    print(f"\n  {SUCCESS}Best match: {best}{RESET}\n")


# =========================================================
# ARGPARSE SETUP
# =========================================================

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="resource_downloader",
        description="SMA-Agent Resource Downloader — download media from 9 pipelines via CLI.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
examples:
  %(prog)s download --pipeline pexels_image --search "cyberpunk city" --count 40
  %(prog)s download --pipeline yt_dlp_video --search "https://youtu.be/dQw4w9WgXcQ"
  %(prog)s download --pipeline duckduckgo --search "ferrari wallpaper" --count 20
  %(prog)s list
  %(prog)s list --media video
  %(prog)s search --query "youtube music mp3"
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # ---- download ----
    dl = subparsers.add_parser("download", aliases=["dl", "d"], help="Download media from a pipeline")
    dl.add_argument("-p", "--pipeline", required=True, help="Pipeline name (e.g. pexels_image, yt_dlp_video)")
    dl.add_argument("-s", "--search", required=True, help="Search term or direct URL")
    dl.add_argument("-c", "--count", type=int, default=None, help="Number of items to download (default: pipeline default)")
    dl.add_argument("-o", "--output", type=str, default=None, help="Custom output directory")
    dl.add_argument("-w", "--workers", type=int, default=5, help="Max parallel download threads (default: 5)")
    dl.add_argument("--safe-search", choices=["off", "modest"], default="off", help="Content safety filter")
    dl.add_argument("--debug", action="store_true", help="Enable debug mode (verbose errors)")

    # ---- list ----
    ls = subparsers.add_parser("list", aliases=["ls", "l"], help="List all available pipelines")
    ls.add_argument("-m", "--media", choices=["image", "video", "music", "gifs"], default=None,
                    help="Filter by media type")

    # ---- search ----
    sr = subparsers.add_parser("search", aliases=["find", "f"], help="Find best pipeline for a keyword query")
    sr.add_argument("-q", "--query", required=True, help="Search keywords (e.g. 'youtube music download mp3')")
    sr.add_argument("--strategy", choices=["overlap", "jaccard", "fuzzy"], default="jaccard",
                    help="Matching strategy (default: jaccard)")
    sr.add_argument("--threshold", type=float, default=0.8,
                    help="Fuzzy match threshold 0.0-1.0 (default: 0.8)")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # Resolve aliases
    cmd_map = {
        "download": cmd_download, "dl": cmd_download, "d": cmd_download,
        "list": cmd_list, "ls": cmd_list, "l": cmd_list,
        "search": cmd_search, "find": cmd_search, "f": cmd_search,
    }

    handler = cmd_map.get(args.command)
    if handler:
        handler(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
