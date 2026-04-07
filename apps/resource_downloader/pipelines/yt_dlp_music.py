"""
yt-dlp Music Pipeline
======================
Factory function for downloading music/audio from YouTube and other
platforms via yt-dlp (audio extraction mode).

>>> Registered via @register_pipeline decorator.
>>> Auto-discovered by discover_pipeline() at startup.
"""

from pathlib import Path
from typing import Optional, Literal

from .register import register_pipeline
from .pipeline_types import ConfigPipeline


@register_pipeline(
    name="yt_dlp_music",
    keywords=["yt-dlp", "youtube", "music", "audio", "mp3", "song", "soundtrack", "beat"],
    description="yt-dlp — extract audio/music from YouTube and 1000+ other sites.",
    media_type="music",
    api_calls_per_hour=100,
    d_exec=True
)
def get_yt_dlp_music_config(
    search_term: str,
    item_count: int = 1,
    download_method: Literal['fast', 'safe'] = 'fast',
    output_dir: Optional[Path | str] = None,
    request_limit: int = 100,
    safe_search: Literal['off', 'modest'] = 'off',
    debug: bool = False
) -> ConfigPipeline:
    """
    Factory to create a ConfigPipeline for yt-dlp music/audio downloads.
    """
    return ConfigPipeline(
        safe_search=safe_search,
        search_term=search_term,
        media_type='music',
        debug=debug,
        item_count=item_count,
        download_method=download_method,
        output_dir=output_dir,
        request_limit=request_limit,
        api_name="yt-dlp"
    )
