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

from typing import Callable,Dict,List,Literal,Any
from types import MappingProxyType
from pathlib import Path
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

PIPELINE_REGISTRY : Dict[str,Dict[str,Any]] = {}
ALLOWED_MEDIA_TYPES = {'image', 'video', 'music', 'gifs', 'song'}
__ROOT__ = Path(__file__).resolve().absolute().parents[3]

def register_pipeline(
    name : str ,
    keywords : List[str] | None = None,
    description : None | str = None,
    media_type : Literal[
        'image', 'video', 'music', 'gifs', 'song'] = 'image',
    api_calls_per_hour : None | int = None,
    d_exec : bool = False
) -> Callable:
    """
    Decorator to register a pipeline function.
    """
    import sys
    sys.path.insert(0,str(__ROOT__))
    from config import config
    if config.IMMEDIATE_ERROR_VALIDATION :
        validate_mediatype(mediatype=media_type)

    def decorator(func : Callable) -> Callable:
        PIPELINE_REGISTRY[name] = {
            "func" : func,
            "keywords" : [kw.lower().strip() for kw in keywords] if keywords else [],
            "description" : description,
            "media_type" : media_type,
            "api_calls_per_hour" : api_calls_per_hour,
            "d_exec" : d_exec
        }
        if not config.IMMEDIATE_ERROR_VALIDATION : validate_mediatype(mediatype=media_type)
        return func
    return decorator

def validate_mediatype(mediatype: str) :
    if mediatype not in ALLOWED_MEDIA_TYPES:
        raise ValueError(f"Invalid media_type: {mediatype}")

def get_pipeline_by_name(name : str ) -> Dict[str,Any] | None:
    """
    Directly retrieve a pipeline by its unique name.
    
    Args:
        name: The unique string ID of the pipeline.
        
    Returns:
        The pipeline metadata dict, or None if not found.
    """
    return PIPELINE_REGISTRY.get(name)

def get_all_pipelines() -> MappingProxyType[str,Dict[str,Any]] :
    """Get all registered pipelines."""
    return MappingProxyType(PIPELINE_REGISTRY)

def get_pipelines_by_media(
    media_type : Literal['image','video','music','gifs','song']
    ) -> List[str]:
    """
    Returns a list of pipeline names that match the given media type.
    """
    return [name for name, data in PIPELINE_REGISTRY.items() if data.get('media_type') == media_type]

def get_pipelines_names() -> List[str] :
    """
    Returns a list of registered pipelines to the user.
    """
    return list(PIPELINE_REGISTRY.keys())

def get_pipeline_by_keywords(params: str | List[str]) -> Dict[str, float]:
    """
    Returns pipeline names with confidence scores based on keyword overlap.

    The score is the fraction of the pipeline's keywords that appear in the
    query, i.e.  ``|intersection| / |pipeline_keywords|``.

    Args:
        params: A search string (split on whitespace) or an explicit keyword list.

    Returns:
        A dict of ``{pipeline_name: confidence}`` sorted descending by score.
    """
    query_keywords = (
        params.lower().split() if isinstance(params, str)
        else [p.lower().strip() for p in params]
    )

    results: Dict[str, float] = {}

    for name, data in PIPELINE_REGISTRY.items():
        pipeline_keywords = data.get("keywords", [])
        if not pipeline_keywords:
            continue

        matches = sum(1 for kw in pipeline_keywords if kw in query_keywords)
        if matches == 0:
            continue

        score = matches / len(pipeline_keywords)
        results[name] = round(score, 4)

    return dict(sorted(results.items(), key=lambda x: x[1], reverse=True))


def _jaccard_similarity(set_a: set, set_b: set) -> float:
    """Compute the Jaccard similarity between two sets: |A ∩ B| / |A ∪ B|."""
    if not set_a and not set_b:
        return 0.0
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union)


def get_pipeline_by_keywords_using_jaccard(params: str | List[str]) -> Dict[str, float]:
    """
    Returns pipeline names with confidence scores using Jaccard similarity.

    Jaccard = |query ∩ pipeline_kw| / |query ∪ pipeline_kw|.
    This penalises queries that are much broader or narrower than the
    pipeline's keyword set, giving a more balanced ranking than simple overlap.

    Args:
        params: A search string (split on whitespace) or an explicit keyword list.

    Returns:
        A dict of ``{pipeline_name: confidence}`` sorted descending by score.
    """
    query_keywords = (
        set(params.lower().split()) if isinstance(params, str)
        else set(p.lower().strip() for p in params)
    )

    results: Dict[str, float] = {}

    for name, data in PIPELINE_REGISTRY.items():
        pipeline_keywords = set(data.get("keywords", []))
        if not pipeline_keywords:
            continue
        score = _jaccard_similarity(query_keywords, pipeline_keywords)
        if score > 0:
            results[name] = round(score, 3)

    return dict(sorted(results.items(), key=lambda x: x[1], reverse=True))

def discover_pipeline():
    """
    Import all pipeline modules to trigger their @register_pipeline decorators.
    Call this once at startup before using the registry.
    """
    # Import all pipeline modules - their decorators auto-register
    from . import (   # type: ignore
        pixels
    )
    
# Auto-discover on import (optional - can also call discover_pipelines() manually)
# discover_pipeline()  # Uncomment to auto-discover


