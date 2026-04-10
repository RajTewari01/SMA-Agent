"""
engine.py — Resource Downloader Engine.

The central orchestrator that:
    1. Discovers all registered pipelines on startup
    2. Routes download requests to the correct API gatherer
    3. Handles parallel file downloads via ThreadPoolExecutor
    4. Manages output directories per media type

Usage:
    >>> from apps.resource_downloader.engine import ResourceDownloaderEngine
    >>> engine = ResourceDownloaderEngine()
    >>> result = engine.download("pexels_image", search_term="cyberpunk city", item_count=10)
    >>> print(result)  # Path to download folder
"""

import logging
import re
import sys
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Literal, Optional, Tuple

__ROOT__ = Path(__file__).resolve().absolute().parents[2]
sys.path.insert(0, str(__ROOT__))

from core.paths import ASSETS_MAP
from core.styling import (
    BOLD, RESET, SUCCESS, WARNING, ERROR, INFO,
    apply_style, Palette,
)

from apps.resource_downloader.pipelines.base import BaseGatherer
from apps.resource_downloader.pipelines.register import (
    PIPELINE_REGISTRY,
    discover_pipeline,
    get_pipeline_by_name,
)
from apps.resource_downloader.pipelines.pipeline_types import ConfigPipeline

logger = logging.getLogger(__name__)


# =========================================================
# API ENDPOINT CONFIGS
# =========================================================

_API_ENDPOINTS = {
    "Pexels": {
        "image": "https://api.pexels.com/v1/search",
        "video": "https://api.pexels.com/videos/search",
    },
    "Unsplash": {
        "image": "https://api.unsplash.com/search/photos",
    },
    "Pixabay": {
        "image": "https://pixabay.com/api/",
        "video": "https://pixabay.com/api/videos/",
    },
    "Giphy": {
        "gifs": "https://api.giphy.com/v1/gifs/search",
    },
}


class ResourceDownloaderEngine:
    """
    Central engine for downloading media resources from multiple APIs.

    Workflow:
        1. Call engine.download(pipeline_name, search_term)
        2. Engine gets the ConfigPipeline from the registry
        3. Dispatches to the correct gatherer based on api_name
        4. Gatherer fetches URLs from the API
        5. Engine downloads files in parallel via ThreadPoolExecutor
        6. Returns the output directory path
    """

    def __init__(self, max_workers: int = 5, debug: bool = False):
        discover_pipeline()
        self.max_workers = max_workers
        self.debug = debug
        self._gatherer = BaseGatherer()

        # Dispatch map: api_name -> gatherer method
        self._dispatch = {
            "Pexels": self._gather_pexels,
            "Unsplash": self._gather_unsplash,
            "Pixabay": self._gather_pixabay,
            "DuckDuckGo": self._gather_duckduckgo,
            "Giphy": self._gather_giphy,
            "yt-dlp": self._gather_ytdlp,
        }

        print(apply_style(
            f"ResourceDownloaderEngine initialized — {len(PIPELINE_REGISTRY)} pipelines loaded",
            BOLD, Palette.GOLD,
        ))

    # =============================================================
    # PUBLIC API
    # =============================================================

    def download(
        self,
        pipeline_name: str,
        search_term: str,
        item_count: Optional[int] = None,
        output_dir: Optional[Path | str] = None,
        safe_search: Literal["off", "modest"] = "off",
    ) -> Optional[Path]:
        """
        Main entry point — download media using a named pipeline.

        Smart duplicate detection:
            Before downloading, scans the output directory for existing
            folders matching the search term. If enough files already
            exist, the download is skipped entirely. If fewer exist
            than requested, only the remaining count is downloaded.
            yt-dlp pipelines are exempt and always download.

        Args:
            pipeline_name: Registered pipeline name (e.g. 'pexels_image', 'yt_dlp_video').
            search_term: What to search for.
            item_count: Override the default item count.
            output_dir: Override the default output directory.
            safe_search: Content safety filter.

        Returns:
            Path to the output directory, or None on failure.
        """
        # 1. Lookup pipeline
        pipeline_data = get_pipeline_by_name(pipeline_name)
        if not pipeline_data:
            print(f"{ERROR}Pipeline '{pipeline_name}' not found.{RESET}")
            return None

        # 2. Build config via the factory function
        factory_fn = pipeline_data["func"]
        media_type = pipeline_data["media_type"]

        # Build a ConfigPipeline by calling the factory
        kwargs = {"search_term": search_term, "safe_search": safe_search}
        if item_count is not None:
            kwargs["item_count"] = item_count

        # Resolve output dir: explicit > ASSETS_MAP
        if output_dir:
            resolved_dir = Path(output_dir)
        else:
            resolved_dir = ASSETS_MAP.get(media_type, ASSETS_MAP.get("image"))
        kwargs["output_dir"] = resolved_dir

        config: ConfigPipeline = factory_fn(**kwargs)
        api_name = config.api_name

        print(f"\n{INFO}Pipeline:{RESET} {pipeline_name}")
        print(f"{INFO}API:{RESET}      {api_name}")
        print(f"{INFO}Search:{RESET}   {config.search_term}")
        print(f"{INFO}Count:{RESET}    {config.item_count}")
        print(f"{INFO}Output:{RESET}   {config.output_dir}\n")

        # 3. Smart duplicate check (skip for yt-dlp — always downloads)
        if api_name != "yt-dlp":
            existing_count, existing_dir = self._check_existing_files(
                config.search_term, Path(config.output_dir)
            )
            if existing_count >= config.item_count:
                print(f"{SUCCESS}Already have {existing_count} files for "
                      f"'{config.search_term}' — skipping download.{RESET}")
                print(f"{INFO}Existing folder:{RESET} {existing_dir}")
                return existing_dir
            elif existing_count > 0:
                needed = config.item_count - existing_count
                print(f"{WARNING}Found {existing_count} existing files for "
                      f"'{config.search_term}' — downloading {needed} more.{RESET}")
                config.item_count = needed

        # 4. Dispatch to the correct gatherer
        gatherer = self._dispatch.get(api_name)
        if not gatherer:
            print(f"{ERROR}No gatherer found for API: {api_name}{RESET}")
            return None

        try:
            result = gatherer(config)
            if result:
                print(f"\n{SUCCESS}Download complete → {result}{RESET}\n")
            return result
        except Exception as e:
            logger.error(f"Download failed for {pipeline_name}: {e}")
            if self.debug:
                raise
            print(f"{ERROR}Download failed: {e}{RESET}")
            return None

    # =============================================================
    # PARALLEL FILE DOWNLOADER
    # =============================================================

    def _download_batch(
        self,
        urls: List[str],
        output_dir: Path,
        headers: Optional[Dict[str, str]] = None,
        prefix: str = "file",
    ) -> Path:
        """
        Download a list of URLs in parallel using ThreadPoolExecutor.

        Args:
            urls: List of direct download URLs.
            output_dir: Directory to save files to.
            headers: Headers to use for each download.
            prefix: Filename prefix.

        Returns:
            The output directory path.
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        total = len(urls)

        def _download_single(args):
            idx, url = args
            ext = url.split("?")[0].split(".")[-1]
            if ext not in ("jpg", "jpeg", "png", "webp", "gif", "mp4", "mp3", "wav"):
                ext = "jpg"
            uid = uuid.uuid4().hex[:5]
            filename = f"{prefix}_{idx:03d}_{uid}.{ext}"
            dest = output_dir / filename

            ok = self._gatherer.download_file(url, dest, headers=headers)
            if ok:
                print(f"  {SUCCESS}[{idx + 1}/{total}]{RESET} {filename}")
            else:
                print(f"  {ERROR}[{idx + 1}/{total}]{RESET} FAILED — {url[:60]}")
            return ok

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = list(executor.map(_download_single, enumerate(urls)))

        succeeded = sum(1 for r in futures if r)
        print(f"\n  Downloaded {succeeded}/{total} files to {output_dir.name}/")
        return output_dir

    # =============================================================
    # PER-API GATHERERS
    # =============================================================

    def _gather_pexels(self, config: ConfigPipeline) -> Optional[Path]:
        """Gather images or videos from Pexels API."""
        headers = self._gatherer.get_headers("Pexels")
        media = config.media_type  # "image" or "video"
        endpoint = _API_ENDPOINTS["Pexels"].get(media)
        if not endpoint:
            print(f"{ERROR}Pexels doesn't support media type: {media}{RESET}")
            return None

        # Paginate to collect enough results
        urls = []
        page = 1
        while len(urls) < config.item_count:
            remaining = config.item_count - len(urls)
            per_page = min(remaining, 80)
            params = {"query": config.search_term, "per_page": per_page, "page": page}

            data = self._gatherer.fetch_json(endpoint, headers=headers, params=params)
            if not data:
                break

            if media == "image":
                photos = data.get("photos", [])
                if not photos:
                    break
                urls.extend(p["src"]["original"] for p in photos)
            else:
                videos = data.get("videos", [])
                if not videos:
                    break
                for v in videos:
                    # Pick the best quality video file
                    hd = next((f for f in v["video_files"] if f.get("quality") == "hd"), None)
                    link = hd["link"] if hd else v["video_files"][0]["link"]
                    urls.append(link)
            page += 1

        if not urls:
            print(f"{WARNING}No results from Pexels for '{config.search_term}'{RESET}")
            return None

        # Create unique output subfolder
        out = self._make_output_dir(config, "pexels")
        return self._download_batch(urls[:config.item_count], out, prefix=config.search_term.replace(" ", "_"))

    def _gather_unsplash(self, config: ConfigPipeline) -> Optional[Path]:
        """Gather images from Unsplash API."""
        headers = self._gatherer.get_headers("Unsplash")
        endpoint = _API_ENDPOINTS["Unsplash"]["image"]

        urls = []
        page = 1
        while len(urls) < config.item_count:
            remaining = config.item_count - len(urls)
            per_page = min(remaining, 30)  # Unsplash max is 30
            params = {"query": config.search_term, "per_page": per_page, "page": page}

            data = self._gatherer.fetch_json(endpoint, headers=headers, params=params)
            if not data:
                break

            results = data.get("results", [])
            if not results:
                break
            urls.extend(r["urls"]["raw"] for r in results)
            page += 1

        if not urls:
            print(f"{WARNING}No results from Unsplash for '{config.search_term}'{RESET}")
            return None

        out = self._make_output_dir(config, "unsplash")
        return self._download_batch(urls[:config.item_count], out, prefix=config.search_term.replace(" ", "_"))

    def _gather_pixabay(self, config: ConfigPipeline) -> Optional[Path]:
        """Gather images or videos from Pixabay API."""
        api_key = self._gatherer.load_api_key("Pixabay")
        if not api_key:
            print(f"{ERROR}Pixabay API key not found in secrets.env.local{RESET}")
            return None

        media = config.media_type
        endpoint = _API_ENDPOINTS["Pixabay"].get(media)
        if not endpoint:
            # Pixabay maps: image → /api/, video → /api/videos/
            endpoint = _API_ENDPOINTS["Pixabay"]["image"]

        headers = self._gatherer.get_headers("Pixabay")
        urls = []
        page = 1
        while len(urls) < config.item_count:
            remaining = config.item_count - len(urls)
            per_page = min(remaining, 200)  # Pixabay max is 200
            params = {
                "key": api_key,
                "q": config.search_term,
                "per_page": per_page,
                "page": page,
                "safesearch": "true" if config.safe_search == "modest" else "false",
            }
            if media == "image":
                params["image_type"] = "photo"

            data = self._gatherer.fetch_json(endpoint, headers=headers, params=params)
            if not data:
                break

            hits = data.get("hits", [])
            if not hits:
                break

            if media == "image":
                urls.extend(h["largeImageURL"] for h in hits)
            else:
                for h in hits:
                    vids = h.get("videos", {})
                    best = vids.get("large") or vids.get("medium") or vids.get("small")
                    if best:
                        urls.append(best["url"])
            page += 1

        if not urls:
            print(f"{WARNING}No results from Pixabay for '{config.search_term}'{RESET}")
            return None

        out = self._make_output_dir(config, "pixabay")
        return self._download_batch(urls[:config.item_count], out, prefix=config.search_term.replace(" ", "_"))

    def _gather_duckduckgo(self, config: ConfigPipeline) -> Optional[Path]:
        """Gather images from DuckDuckGo search (no API key needed)."""
        try:
            from ddgs import DDGS
        except ImportError:
            print(f"{ERROR}ddgs package not installed. Run: pip install ddgs{RESET}")
            return None

        print(f"  Searching DuckDuckGo for '{config.search_term}'...")
        with DDGS() as ddgs:
            results = list(ddgs.images(
                query=config.search_term,
                max_results=config.item_count,
                safesearch=config.safe_search,
                region="us-en",
                type_image="photo",
            ))

        if not results:
            print(f"{WARNING}No results from DuckDuckGo for '{config.search_term}'{RESET}")
            return None

        urls = [r["image"] for r in results]
        headers = self._gatherer.get_headers("DuckDuckGo")
        out = self._make_output_dir(config, "duckduckgo")
        return self._download_batch(urls, out, headers=headers, prefix=config.search_term.replace(" ", "_"))

    def _gather_giphy(self, config: ConfigPipeline) -> Optional[Path]:
        """Gather GIFs/videos from Giphy API."""
        api_key = self._gatherer.load_api_key("Giphy")
        if not api_key:
            print(f"{ERROR}Giphy API key not found in secrets.env.local{RESET}")
            return None

        headers = self._gatherer.get_headers("Giphy")
        endpoint = _API_ENDPOINTS["Giphy"]["gifs"]

        params = {
            "api_key": api_key,
            "q": config.search_term,
            "limit": min(config.item_count, 50),
            "rating": "g" if config.safe_search == "modest" else "r",
        }

        data = self._gatherer.fetch_json(endpoint, headers=headers, params=params)
        if not data or not data.get("data"):
            print(f"{WARNING}No results from Giphy for '{config.search_term}'{RESET}")
            return None

        # Prefer mp4 for video, fall back to gif url
        urls = []
        for entry in data["data"]:
            mp4 = entry.get("images", {}).get("original", {}).get("mp4")
            if mp4:
                urls.append(mp4)
            else:
                gif_url = entry.get("images", {}).get("original", {}).get("url")
                if gif_url:
                    urls.append(gif_url)

        if not urls:
            print(f"{WARNING}No downloadable GIFs found{RESET}")
            return None

        out = self._make_output_dir(config, "giphy")
        return self._download_batch(urls, out, prefix=config.search_term.replace(" ", "_"))

    def _gather_ytdlp(self, config: ConfigPipeline) -> Optional[Path]:
        """Download video or audio using yt-dlp."""
        try:
            import yt_dlp
        except ImportError:
            print(f"{ERROR}yt-dlp not installed. Run: pip install yt-dlp{RESET}")
            return None

        out = self._make_output_dir(config, "ytdlp")
        uid = uuid.uuid4().hex[:6]
        safe_term = config.search_term.replace(" ", "_").replace("/", "_")[:40]

        is_url = config.search_term.startswith(("http://", "https://"))

        if config.media_type == "music":
            # Audio extraction mode
            outtmpl = str(out / f"{safe_term}_{uid}.%(ext)s")
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": outtmpl,
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
                "quiet": not self.debug,
                "no_warnings": not self.debug,
                "retries": 5,
            }
        else:
            # Video download mode
            outtmpl = str(out / f"{safe_term}_{uid}.%(ext)s")
            ydl_opts = {
                "format": "bestvideo+bestaudio/best",
                "outtmpl": outtmpl,
                "quiet": not self.debug,
                "no_warnings": not self.debug,
                "retries": 5,
                "merge_output_format": "mp4",
                "extractor_args": {
                    "youtube": {
                        "player_client": ["android", "web"],
                    }
                },
            }

        if is_url:
            # Direct URL download
            target = config.search_term
        else:
            # Search for a video using ytsearch
            target = f"ytsearch{config.item_count}:{config.search_term}"

        try:
            print(f"  yt-dlp downloading: {target[:80]}...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([target])
            print(f"  {SUCCESS}yt-dlp download complete{RESET}")
            return out
        except Exception as e:
            logger.error(f"yt-dlp failed: {e}")
            if self.debug:
                raise
            print(f"{ERROR}yt-dlp failed: {e}{RESET}")
            return None

    # =============================================================
    # HELPERS
    # =============================================================

    @staticmethod
    def _normalize_term(term: str) -> str:
        """Normalize a search term into a folder-safe, comparable string."""
        t = term.lower().strip()
        t = re.sub(r"[^a-z0-9]+", "_", t)
        return t.strip("_")

    def _check_existing_files(
        self, search_term: str, base_dir: Path
    ) -> Tuple[int, Optional[Path]]:
        """
        Scan base_dir for existing folders matching the search term
        using rglob. Count media files inside.

        Args:
            search_term: The original search query.
            base_dir: The media-type root dir (e.g. assets/image/).

        Returns:
            (file_count, matching_folder_path) — (0, None) if no match.
        """
        if not base_dir.exists():
            return 0, None

        norm = self._normalize_term(search_term)
        if not norm:
            return 0, None

        _MEDIA_EXTS = {
            ".jpg", ".jpeg", ".png", ".webp", ".gif",
            ".mp4", ".mkv", ".webm", ".mov",
            ".mp3", ".wav", ".ogg", ".m4a",
        }

        best_count = 0
        best_dir = None

        # Walk immediate subdirectories — folders are named like
        # "pexels_ferrari_a1b2c3" or "duckduckgo_dark_forest_x9y8z7"
        for folder in base_dir.iterdir():
            if not folder.is_dir():
                continue
            folder_norm = self._normalize_term(folder.name)
            # Match if the normalized search term appears in the folder name
            if norm in folder_norm:
                count = sum(
                    1 for f in folder.rglob("*")
                    if f.is_file() and f.suffix.lower() in _MEDIA_EXTS
                )
                if count > best_count:
                    best_count = count
                    best_dir = folder

        return best_count, best_dir

    @staticmethod
    def _make_output_dir(config: ConfigPipeline, source_tag: str) -> Path:
        """
        Get or create the output subdirectory for a download batch.

        If an existing folder matching the search term is found under
        the output root, it will be reused. Otherwise a new folder
        is created with pattern: {source_tag}_{search_term}_{uid}
        """
        safe_term = (config.search_term or "download").replace(" ", "_")[:30]
        base = Path(config.output_dir)

        # Try to find an existing folder matching this search term
        norm = re.sub(r"[^a-z0-9]+", "_", safe_term.lower()).strip("_")
        if base.exists():
            for folder in base.iterdir():
                if folder.is_dir() and norm in folder.name.lower():
                    return folder  # Reuse existing folder

        # No match found — create a new one
        uid = uuid.uuid4().hex[:6]
        folder_name = f"{source_tag}_{safe_term}_{uid}"
        out = base / folder_name
        out.mkdir(parents=True, exist_ok=True)
        return out
