"""
PIPELINE REGISTRY SYSTEM
==========================

NOTE : A central registry for managing media generation pipelines.
This system allows developers to register new pipeline configurations
using a simple decorator, eliminating the need to modify core logic
when adding new styles or capabilities.

>>> USAGE :
            @register_pipeline(
            name = "Pixels_immage",
            keywords=["keyword1", "keyword2"]
            description = "A online library for highly curated high-res stock photos.",
            media_type = "image",
            api_calls_per_hour = 100,
            d_exec = True
            )
            def pipeline_name(*args, **kwargs):
                pass
"""

import re
from collections.abc import Mapping
from difflib import SequenceMatcher
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable, Dict, List, Literal

"""
 ==================GLOBAL REGISTRY SYSTEM STORAGE=====================
Features :
            >>> Stores metadata for a particular pipeline.
            >>> stores factory function for all registered pipeline.
Structures :
            >>>
            { pipeline_name :
                {
                    "name" : str
                    "keywords" : List[str],
                    "description" : str,
                    "media_type" : Literal['image', 'video','music','song','gifs'],
                    "api_calls_per_hour" : int,
                    "d_exec" : bool
                }
            }
            or
            PIPELINE_REGISTRY[name] = {
                "func" : func,
                "name" : name,
                "keywords" : keywords,
                "description" : description,
                "media_type" : media_type,
                "api_calls_per_hour" : api_calls_per_hour,
                "d_exec" : d_exec
            }

            >>> Short : { pipeline_name : { function : <Callable> ,keywords : List[str],.....}}

"""

PIPELINE_REGISTRY: Dict[str, Dict[str, Any]] = {}
ALLOWED_MEDIA_TYPES = {"image", "video", "music", "gifs", "song"}
__ROOT__ = Path(__file__).resolve().absolute().parents[3]


def register_pipeline(
    name: str,
    keywords: List[str] | None = None,
    description: None | str = None,
    media_type: Literal["image", "video", "music", "gifs", "song"] = "image",
    api_calls_per_hour: None | int = None,
    d_exec: bool = False,
) -> Callable:
    """
    Decorator to register a pipeline function.
    """
    import sys

    sys.path.insert(0, str(__ROOT__))
    from config import config

    if config.IMMEDIATE_ERROR_VALIDATION:
        validate_mediatype(mediatype=media_type)

    def decorator(func: Callable) -> Callable:
        PIPELINE_REGISTRY[name] = {
            "func": func,
            "keywords": [kw.lower().strip() for kw in keywords] if keywords else [],
            "description": description,
            "media_type": media_type,
            "api_calls_per_hour": api_calls_per_hour,
            "d_exec": d_exec,
        }
        if not config.IMMEDIATE_ERROR_VALIDATION:
            validate_mediatype(mediatype=media_type)
        return func

    return decorator


def validate_mediatype(mediatype: str):
    if mediatype not in ALLOWED_MEDIA_TYPES:
        raise ValueError(f"Invalid media_type: {mediatype}")


def get_pipeline_by_name(name: str) -> Dict[str, Any] | None:
    """
    Directly retrieve a pipeline by its unique name.

    Args:
        name: The unique string ID of the pipeline.

    Returns:
        The pipeline metadata dict, or None if not found.
    """
    return PIPELINE_REGISTRY.get(name)


def get_all_pipelines() -> Mapping[str, Dict[str, Any]]:
    """Get all registered pipelines."""
    return MappingProxyType(PIPELINE_REGISTRY)


def get_pipelines_by_media(media_type: Literal["image", "video", "music", "gifs", "song"]) -> List[str]:
    """
    Returns a list of pipeline names that match the given media type.
    """
    return [name for name, data in PIPELINE_REGISTRY.items() if data.get("media_type") == media_type]


def get_pipelines_names() -> List[str]:
    """
    Returns a list of registered pipelines to the user.
    """
    return list(PIPELINE_REGISTRY.keys())


def _jaccard_similarity(set_a: set, set_b: set) -> float:
    """Compute the Jaccard similarity between two sets: |A ∩ B| / |A ∪ B|."""
    if not set_a and not set_b:
        return 0.0
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union)


def _tokenize(text: str) -> List[str]:
    """
    Extract unique, lowercased word tokens from a string.

    Strips punctuation / special characters and returns only
    alphanumeric tokens (no duplicates).
    """
    return list(set(re.findall(r"[a-zA-Z0-9]+", text.lower().strip())))


def _fuzzy_match(a: str, b: str, threshold: float = 0.8) -> bool:
    """Return True if SequenceMatcher ratio between *a* and *b* >= *threshold*."""
    return SequenceMatcher(None, a, b).ratio() >= threshold


def get_pipeline_by_keywords(
    params: str | List[str], strategy: Literal["overlap", "jaccard", "fuzzy"] = "jaccard", fuzzy_threshold: float = 0.8
) -> Dict[str, float]:
    """
    Returns pipeline names ranked by keyword similarity.

    Strategies:
        overlap  — |matches| / |pipeline_keywords|.
                   Good when you want to know how much of a pipeline's
                   identity the query covers.
        jaccard  — |query ∩ kw| / |query ∪ kw|  (default).
                   Penalises overly broad or narrow queries, giving a
                   more balanced ranking.
        fuzzy    — Uses SequenceMatcher to find approximate matches.
                   Catches typos like "pixle" → "pexels" or
                   "unsplsh" → "unsplash".

    Args:
        params:          A search string (split on whitespace) or a keyword list.
        strategy:        Scoring algorithm — ``'overlap'``, ``'jaccard'``, or ``'fuzzy'``.
        fuzzy_threshold: Minimum SequenceMatcher ratio to count as a match
                         (only used when ``strategy='fuzzy'``). Default 0.8.

    Returns:
        A dict of ``{pipeline_name: confidence}`` sorted descending by score.
    """
    # --- Tokenize the query ---
    if isinstance(params, str):
        query_tokens = _tokenize(params)
    else:
        query_tokens = [p.lower().strip() for p in params]

    results: Dict[str, float] = {}

    for name, data in PIPELINE_REGISTRY.items():
        pipeline_keywords = data.get("keywords", [])
        if not pipeline_keywords:
            continue

        if strategy == "jaccard":
            score = _jaccard_similarity(set(query_tokens), set(pipeline_keywords))

        elif strategy == "fuzzy":
            matches = 0
            for kw in pipeline_keywords:
                for qt in query_tokens:
                    if _fuzzy_match(qt, kw, threshold=fuzzy_threshold):
                        matches += 1
                        break
            if matches == 0:
                continue
            score = matches / len(pipeline_keywords)

        else:  # overlap
            matches = sum(1 for kw in pipeline_keywords if kw in query_tokens)
            if matches == 0:
                continue
            score = matches / len(pipeline_keywords)

        if score > 0:
            results[name] = round(score, 4)

    return dict(sorted(results.items(), key=lambda x: x[1], reverse=True))


def discover_pipeline():
    """
    Import all pipeline modules to trigger their @register_pipeline decorators.
    Call this once at startup before using the registry.

    Registered Pipelines:
        >>> pexels_image    — Pexels stock photos          (image)
        >>> pexels_video    — Pexels stock video clips      (video)
        >>> pixabay_image   — Pixabay royalty-free images   (image)
        >>> pixabay_video   — Pixabay royalty-free videos   (video)
        >>> giphy           — Giphy animated GIFs           (gifs)
        >>> unsplash        — Unsplash creative photos      (image)
        >>> duckduckgo      — DuckDuckGo web image search   (image)
        >>> yt_dlp_video    — yt-dlp video downloads        (video)
        >>> yt_dlp_music    — yt-dlp audio/music extraction (music)
    """
    from . import (  # type: ignore
        duckduckgo,  # duckduckgo
        giphy,  # giphy
        pixabay,  # pixabay_image
        pixabay_video,  # pixabay_video
        pixels,  # pexels_image
        pixels_video,  # pexels_video
        unsplash,  # unsplash
        yt_dlp_music,  # yt_dlp_music
        yt_dlp_video,  # yt_dlp_video
    )
