from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from sys import path
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, model_validator

__ROOT__ = Path(__file__).resolve().absolute().parents[1]
path.insert(0, str(__ROOT__))
from core.paths import get_venv_mapping


class ModelType(str, Enum):
    OFFLINE = "offline"
    ONLINE = "online"


class BaseConfig(BaseModel):
    model_path: str
    model_type: ModelType

    @model_validator(mode="after")
    def validate_logic(self):
        if self.model_type == ModelType.OFFLINE:
            if not self.model_path:
                raise ValueError("Model path is required for offline model")
            if not Path(self.model_path).exists():
                raise FileNotFoundError(f"Model path not found: {self.model_path}")
        return self


class BaseInference(ABC):
    """
    Abstract base class for all inference pipelines.

    Defines a strict pipeline:
        preprocess → generate → postprocess → validate
    """

    def __init__(self, config: BaseConfig):
        self.config = config
        self.model = None
        self.llm_venv_path = get_venv_mapping().get("ai")

    # ============ LLM LIFECYCLE ============

    @abstractmethod
    def load_model(self) -> None:
        """load the model"""
        pass

    def preprocess(self, prompts: str) -> str:
        """preprocessing the prompt"""
        return prompts.strip()

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Run inference on the model."""
        pass

    def validate_output(self, output: Any) -> bool:
        return True

    def postprocess(self, output: Any) -> Any:
        return output

    # =========== api endpoint =================
    def run(self, prompt: str, **kwargs) -> Any:
        prompt = self.preprocess(prompt)
        raw = self.generate(prompt, **kwargs)
        output = self.postprocess(raw)

        if not self.validate_output(output):
            raise ValueError("Invalid output")

        return output
