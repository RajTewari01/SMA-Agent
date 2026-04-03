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


