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

import json
import re
import sqlite3
import sys
from logging import error
from pathlib import Path
from typing import Dict, Literal, Optional, Tuple, TypedDict
from warnings import warn

from llama_cpp import Llama
from pydantic import BaseModel, EncodedBytes, Field
from torch import cuda

from core.styling import apply_style

__ROOT__ = Path(__file__).resolve().parents[2].absolute()
sys.path.insert(0, str(__ROOT__))
from config import config
from core.base_inference import BaseInference
from core.paths import DB_DIR, STORIES_JSON, STORY_GRAMMARS_SCHEMA, get_venv_mapping
from core.styling import *


class StoryInfernece(BaseInference):
    def __init__(self, llm_venv_path, load_model=True):
        self.llm_grammar = STORY_GRAMMARS_SCHEMA
        self.db_path = DB_DIR
        self.db_connection = sqlite3.connect(self.db_path / "story_teller.db")
        self.cursor = self.db_connection.cursor()
        self.app_environment = config.CONFIG_TYPE
        self.debug = config.DEBUG
        self._init_db()
        self.llm = None
        self.llm_path = None

        if load_model:
            print(apply_style("Loading Model...", Style.BOLD, Palette.GOLD))
            self.llm = self.load_model()

        super().__init__(llm_venv_path)

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

    def unload_model(self):
        if self.llm:
            del self.llm
            self.llm = None
            import gc

            gc.collect()
            if cuda.is_available():
                cuda.empty_cache()

    def load_model(self):
        return Llama(model_path=str(self.llm_path), n_ctx=3086, n_gpu_layers=-1, verbose=False)

    def sync_json_to_db(self):
        try:
            count = 0
            with open(STORIES_JSON, "r", encoding="utf-8", errors="ignore") as infile:
                data = json.load(infile)
            for key, value in data.get("stories", {}).items():
                self.cursor.execute("INSERT OR IGNORE INTO stories (id, content) VALUES (?, ?)", (story_id, story_data))
                if self.cursor.rowcount > 0:
                    count += 1

            self.db_connection.commit()
            if count > 0:
                print(f"Synced {count} new prompts to database.")

        except Exception as e:
            if self.debug:
                raise (f"{ERROR}Error occured{RESET}") from e
            else:
                warn(f"{ERROR}Error: {e}{RESET}")
                return None

    def get_prompt_from_db(self) -> Tuple[Optional[str], Optional[str]]:
        self.cursor.execute("SELECT id, content FROM stories WHERE posted = 0 ORDER BY RANDOM() LIMIT 1")
        result = self.cursor.fetchone()
        if result:
            return result[0], result[1]
        return None, None

    def get_history(self, limit=3) -> str:
        """Fetches the titles of the last few posted stories to avoid repetition."""
        try:
            self.cursor.execute("SELECT content FROM stories WHERE posted = 1 ORDER BY rowid DESC LIMIT ?", (limit,))
            rows = self.cursor.fetchall()
            if not rows:
                return "No previous stories."
            return "\n".join([f"- {row[0]}" for row in rows])
        except Exception:
            return "No history available."

    def mark_as_posted(self, story_id: str, final_output: str):
        if story_id:
            self.cursor.execute(
                "UPDATE stories SET posted = 1, generated_output = ? WHERE id = ?", (final_output, story_id)
            )
            self.db_connection.commit()
