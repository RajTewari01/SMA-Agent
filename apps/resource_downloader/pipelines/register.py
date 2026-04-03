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

from typing import Callable,Tuple,Dict,List,Literal,Any
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
    if media_type not in ALLOWED_MEDIA_TYPES:
        raise ValueError(f"Invalid media_type: {media_type}")

    def decorator(func : Callable) -> Callable:
        PIPELINE_REGISTRY[name] = {
            "func" : func,
            "keywords" : [kw.lower().strip() for kw in keywords] if keywords else [],
            "description" : description,
            "media_type" : media_type,
            "api_calls_per_hour" : api_calls_per_hour,
            "d_exec" : d_exec
        }
        return func
    return decorator

def get_pipeline_by_name(name : str ) -> Dict[str,Any] | None:
    """
    Directly retrieve a pipeline by its unique name.
    
    Args:
        name: The unique string ID of the pipeline.
        
    Returns:
        The pipeline metadata dict, or None if not found.
    """
    return PIPELINE_REGISTRY.get(name)

def get_all_pipelines() -> Dict[str,Dict[str,Any]] :
    """Get all registered pipelines."""
    return PIPELINE_REGISTRY

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
    # or in short list(PIPELINE_REGISTRY.keys())
    return [name for name in PIPELINE_REGISTRY.keys()] # <just for mine> <- IGNORE THIS COMMENT

# def get_pipeline_by_keywords(params: str | List[str]) -> Dict[str, float]:
#     """
#     Returns pipeline names with confidence scores based on keyword overlap.
#     """
#     # normalize input into list
    
#     query_keywords = params.lower().split() if isinstance(params, str) else [p.lower().strip() for p in params]
    
#     results: Dict[str, float] = dict()

#     for name, data in PIPELINE_REGISTRY.items():
#         pipeline_keywords = data.get("keywords", [])
#         if not pipeline_keywords:continue
#         # compute overlap
#         matches = 0
#         for kw in pipeline_keywords:
#             if kw in query_keywords:
#                 matches += 1

#         if matches == 0:
#             continue

#         # confidence score (normalized)
#         score = matches / len(pipeline_keywords)
#         results[name] = round(score,4)
#     # optional: sort by confidence (recommended)
#     results = dict(sorted(results.items(), key=lambda x: x[1], reverse=True))
#     return results
    
# def get_pipeline_by_keywords_using_jaccard(params: str | List[str]) -> Dict[str, float]:

#     query_keywords = set(params.lower().split()) if isinstance(params, str) else set(p.lower().strip() for p in params)
#     results: Dict[str, float] = {}
#     for name, data in PIPELINE_REGISTRY.items():
#         pipeline_keywords = set(data.get("keywords", []))
#         score = jaccard_similarity(query_keywords, pipeline_keywords)
#         if score > 0:
#             results[name] = round(score, 3)
#     return dict(sorted(results.items(), key=lambda x: x[1], reverse=True))

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


