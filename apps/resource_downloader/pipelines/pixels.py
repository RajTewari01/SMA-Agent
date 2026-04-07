"""
Pexels Image Pipeline
======================
Factory function for downloading high-resolution stock images from Pexels.

>>> Registered via @register_pipeline decorator.
>>> Auto-discovered by discover_pipeline() at startup.
"""

from pathlib import Path
from typing import Literal, Optional

from .pipeline_types import ConfigPipeline
from .register import register_pipeline


@register_pipeline(
    name="pexels_image",
    keywords=["pexels", "stock", "photo", "image", "hd", "wallpaper", "high-res"],
    description="Pexels — a curated library for high-resolution stock photos.",
    media_type="image",
    api_calls_per_hour=200,
    d_exec=True
)
def get_pexels_image_config(
    search_term: str,
    item_count: int = 25,
    download_method: Literal['fast', 'safe'] = 'fast',
    output_dir: Optional[Path | str] = None,
    request_limit: int = 200,
    safe_search: Literal['off', 'modest'] = 'off',
    debug: bool = False
) -> ConfigPipeline:
    """
    Factory to create a ConfigPipeline for Pexels image downloads.
    """
    return ConfigPipeline(
        safe_search=safe_search,
        search_term=search_term,
        media_type='image',
        debug=debug,
        item_count=item_count,
        download_method=download_method,
        output_dir=output_dir,
        request_limit=request_limit,
        api_name="Pexels"
    )
