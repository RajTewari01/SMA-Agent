"""
Pixabay Image Pipeline
=======================
Factory function for downloading royalty-free images from Pixabay.

>>> Registered via @register_pipeline decorator.
>>> Auto-discovered by discover_pipeline() at startup.
"""

from pathlib import Path
from typing import Optional, Literal

from .register import register_pipeline
from .pipeline_types import ConfigPipeline


@register_pipeline(
    name="pixabay_image",
    keywords=["pixabay", "royalty-free", "photo", "image", "illustration", "vector"],
    description="Pixabay — royalty-free stock images and illustrations.",
    media_type="image",
    api_calls_per_hour=100,
    d_exec=True
)
def get_pixabay_image_config(
    search_term: str,
    item_count: int = 25,
    download_method: Literal['fast', 'safe'] = 'fast',
    output_dir: Optional[Path | str] = None,
    request_limit: int = 100,
    safe_search: Literal['off', 'modest'] = 'off',
    debug: bool = False
) -> ConfigPipeline:
    """
    Factory to create a ConfigPipeline for Pixabay image downloads.
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
        api_name="Pixabay"
    )
