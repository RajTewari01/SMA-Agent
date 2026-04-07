"""
Giphy GIF/Video Pipeline
==========================
Factory function for downloading GIFs and short video clips from Giphy.

>>> Registered via @register_pipeline decorator.
>>> Auto-discovered by discover_pipeline() at startup.
"""

from pathlib import Path
from typing import Literal, Optional

from .pipeline_types import ConfigPipeline
from .register import register_pipeline


@register_pipeline(
    name="giphy",
    keywords=["giphy", "gif", "animated", "reaction", "meme", "sticker"],
    description="Giphy — the largest library of animated GIFs and stickers.",
    media_type="gifs",
    api_calls_per_hour=42,
    d_exec=True,
)
def get_giphy_config(
    search_term: str,
    item_count: int = 10,
    download_method: Literal["fast", "safe"] = "fast",
    output_dir: Optional[Path | str] = None,
    request_limit: int = 42,
    safe_search: Literal["off", "modest"] = "off",
    debug: bool = False,
) -> ConfigPipeline:
    """
    Factory to create a ConfigPipeline for Giphy GIF downloads.
    """
    return ConfigPipeline(
        safe_search=safe_search,
        search_term=search_term,
        media_type="gifs",
        debug=debug,
        item_count=item_count,
        download_method=download_method,
        output_dir=output_dir,
        request_limit=request_limit,
        api_name="Giphy",
    )
