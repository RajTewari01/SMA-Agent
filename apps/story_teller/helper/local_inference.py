"""
local_inference.py — Story Teller
================================

FEATURES:
    >>> Generates high-quality stories or poems by dynamically adjusting parameters based on user input.

    >>> If the genre or theme is not provided, it automatically retrieves suitable options
        from a JSON file or database and generates coherent content.

    >>> Ensures structured output formatting using Pydantic models and GBNF schemas
        for reliable JSON generation.

    >>> Optimized for low-end systems (e.g., GTX 1650) with efficient inference settings.

NOTES:
    - Replace the local model path with a higher-parameter model for improved quality.
    - Output quality depends heavily on the model used and parameter tuning.
    - GBNF is used to enforce strict output structure (especially useful for JSON consistency).
    - Designed for balance between performance and quality on limited hardware.
"""

from core.styling import apply_style
import sqlite3
import json
import re
import sys
import sqlite3
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Dict, Literal, Optional, Tuple, TypedDict
from llama_cpp import Llama
from torch import cuda

__ROOT__ = Path(__file__).resolve().parents[2].absolute()
sys.path.insert(0, str(__ROOT__))
from config import config 
from core.base_inference import BaseInference
from core.paths import get_venv_mapping,DB_DIR,STORY_GRAMMARS_SCHEMA
from core.styling import *


class StoryInfernece(BaseInference):

    def __init__(
        self,
        llm_venv_path,
        load_model=True):
        self.llm_grammar = STORY_GRAMMARS_SCHEMA
        self.db_path = DB_DIR
        self.db_connection = sqlite3.connect(self.db_path/ "story_teller.db")
        self.cursor = self.db_connection.cursor()
        self.app_environment = config.CONFIG_TYPE
        self.debug = config.DEBUG
        self._init_db()
        self.llm = None
        self.llm_path = None

        if load_model:
            print(apply_style('Loading Model...',Style.BOLD,Palette.GOLD))
            self.llm = self.load_model()

        super().__init__(
            llm_venv_path)
    
    def _init_db(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS story_teller(
                            id TEXT PRIMARY KEY,
                            content TEXT,
                            posted INTEGER DEFAULT 0,
                            generated_output TEXT
                            )
        """)
        self.db_connection.commit()
    
    def unload_model(self) : 
        if self.llm:
            del self.llm
            self.llm = None
            import gc
            gc.collect()
            if cuda.is_available():
                cuda.empty_cache()

    def load_model(self):
        return Llama(
                model_path=str(self.llm_path),
                n_ctx=3086,
                n_gpu_layers=-1, 
                verbose=False
            )
    
    
        
        
