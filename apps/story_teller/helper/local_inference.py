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
import sys
from pathlib import Path
from typing import Dict, Literal, Optional, Tuple, TypedDict

from pydantic import BaseModel, Field

__ROOT__ = Path(__file__).resolve().parents[2].absolute()
sys.path.insert(0, str(__ROOT__))
from core.llm import BaseInference

from config import config
from core.paths import llm_venv_path


class StoryInfernece(BaseInference):
    __slots__ = ["_model_path", "_model_name", "_model_type", "_model_params", "_llm_venv_path", "_llm_env_vars"]

    def __init__(self):
        super().__init__()
