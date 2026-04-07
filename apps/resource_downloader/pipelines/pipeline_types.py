"""
pipelines_types.py -> creates a formal format for all pipelines types to follow.
"""
from typing import Literal,Optional,List
from dataclasses import dataclass,field
from pathlib import Path
import random
import json

__ROOT__ = Path(__file__).resolve().absolute().parents[3]

@dataclass
class ConfigPipeline:
    """
    Configuration dataclass for the downloading pipeline.
    
    This class handles the setup of search parameters, directory management,
    and dynamic defaults for item counts based on media type.
    """
    # --- 1. REQUIRED FIELDS (Must be defined first) ---
    safe_search: Literal['off', 'modest'] ='off'
    search_term: str | None = field(default=None)
    # --- 2. OPTIONAL FIELDS (With defaults) ---
    media_type: Literal['image', 'video','music','song','gifs'] = 'image'
    debug: bool = True
    item_count: Optional[int] = None
    download_method: Literal['fast', 'safe'] = 'fast'
    request_limit: int = 50  # API rate limit buffer per day(Rate limiter)
    output_dir: Path | str | None  = None
    api_name : str = "Internet"

    def __post_init__(self):
        """
        Post-initialization processing:
        1. Converts output_dir to Path and creates it if missing.
        2. Loads a random search term if none is provided.
        3. Sets default item_count based on download_type (Video vs Image).
        """
        
        # --- Handle Output Directory ---
        if self.output_dir:
            # Ensures its a path object and not a string.
            self.output_dir = Path(self.output_dir)
            # Creates the directory if it doesn't exist.
            if not self.output_dir.exists():
                self.output_dir.mkdir(parents=True, exist_ok=True)

        # --- Handle count ---
        DEFAULT_COUNT = {
            'video':5,
            'image':25,
            'gifs':10,
            'music':1,
            'song':1
        }
        if self.item_count is None:
            self.item_count = DEFAULT_COUNT.get(self.media_type,1)

        if self.search_term:
            self.search_term = self._sanitize_searchterm(self.search_term)
        
        if not self.search_term:
            self.search_term = self._load_random_searchterm()

    def _sanitize_searchterm(
            self,
            term :  str
            ) ->str:
            """
            Local sanitizer or lazy wrapper around BaseGatherer.
            Prevents global instantiation of BaseGatherer.

            Features :
                >>> 1. Remove Emojis.
                >>> 2. Remove Special Characters.
                >>> 3. Remove Extra Spaces.
                >>> 4. Convert to Lowercase.
            """
            from sys import path
            path.insert(0,str(__ROOT__))
            from apps.resource_downloader.pipelines.base import BaseGatherer
            return BaseGatherer.sanitize_search_term(term = term)
        
    def _load_random_searchterm(self) -> str:
            """
            Loads a random search term from the search_terms.json file.
            """
            try:
                from sys import path
                path.insert(0,str(__ROOT__))
                from core.paths import SEARCH_QUERIES 
                import json
                with open(SEARCH_QUERIES, "r") as infile:
                    data = json.load(infile)
                    needed_data = random.choice(data.get(self.media_type,[])) 
                    return needed_data

            except ImportError :
                raise ImportError("Please install the required dependencies.")
            except FileNotFoundError :
                raise FileNotFoundError("Please ensure the search_terms.json file exists.")
            except Exception as e:
                raise Exception(f"An error occurred while loading the search terms") from e 

        
