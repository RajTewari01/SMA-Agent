"""
yt-dlp Video Pipeline
======================
Factory function for downloading videos from YouTube and other
platforms via yt-dlp.

>>> Registered via @register_pipeline decorator.
>>> Auto-discovered by discover_pipeline() at startup.
"""

from pathlib import Path
from typing import Literal, Optional

from .pipeline_types import ConfigPipeline
from .register import register_pipeline


@register_pipeline(
    name="yt_dlp_video",
    keywords=["yt-dlp", "youtube", "video", "download", "stream", "clip", "mp4", "webm"],
    description="yt-dlp — download videos from YouTube and 1000+ other sites.",
    media_type="video",
    api_calls_per_hour=100,
    d_exec=True,
)
def get_yt_dlp_video_config(
    search_term: str,
    item_count: int = 5,
    download_method: Literal["fast", "safe"] = "fast",
    output_dir: Optional[Path | str] = None,
    request_limit: int = 100,
    safe_search: Literal["off", "modest"] = "off",
    debug: bool = False,
) -> ConfigPipeline:
    """
    Factory to create a ConfigPipeline for yt-dlp video downloads.
    """
    return ConfigPipeline(
        safe_search=safe_search,
        search_term=search_term,
        media_type="video",
        debug=debug,
        item_count=item_count,
        download_method=download_method,
        output_dir=output_dir,
        request_limit=request_limit,
        api_name="yt-dlp",
    )
