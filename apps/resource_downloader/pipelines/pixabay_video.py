"""
Pixabay Video Pipeline
=======================
Factory function for downloading royalty-free video clips from Pixabay.

>>> Registered via @register_pipeline decorator.
>>> Auto-discovered by discover_pipeline() at startup.
"""

from pathlib import Path
from typing import Literal, Optional

from .pipeline_types import ConfigPipeline
from .register import register_pipeline


@register_pipeline(
    name="pixabay_video",
    keywords=["pixabay", "royalty-free", "video", "clip", "footage", "motion"],
    description="Pixabay — royalty-free stock video clips.",
    media_type="video",
    api_calls_per_hour=100,
    d_exec=True,
)
def get_pixabay_video_config(
    search_term: str,
    item_count: int = 5,
    download_method: Literal["fast", "safe"] = "fast",
    output_dir: Optional[Path | str] = None,
    request_limit: int = 100,
    safe_search: Literal["off", "modest"] = "off",
    debug: bool = False,
) -> ConfigPipeline:
    """
    Factory to create a ConfigPipeline for Pixabay video downloads.
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
        api_name="Pixabay",
    )
