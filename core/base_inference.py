from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from sys import path
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, model_validator

__ROOT__ = Path(__file__).resolve().absolute().parents[1]
path.insert(0, str(__ROOT__))


class ModelType(str, Enum):
    OFFLINE = "offline"
    ONLINE = "online"


class BaseConfig(BaseModel):
    model_path: str
    model_type: ModelType

    @model_validator(mode="after")
    def validate_logic(self):
        if self.model_type == ModelType.OFFLINE:
            if not Path(self.model_path).exists():
                raise FileNotFoundError(f"Model path not found: {self.model_path}")
                raise ValueError("Model path is required for offline model")
        return self


class BaseInference(ABC):
    """
    Abstract base class for all inference pipelines.

    Defines a strict pipeline:
        preprocess → generate → postprocess → validate
    """

    def __init__(self, settings: Dict[str, Any] | None = None):
        self.llm_venv_path = None
        self.settings = settings
        self.model = None

    # ============ LLM LIFECYCLE ============

    @abstractmethod
    def load_model(self, model_path: str | None, model_type: ModelType | None = None) -> None:
        """load the model"""
        pass

    def preprocessing(self, prompts: str) -> str:
        """preprocessing the prompt"""
        import re

    @abstractmethod
    def generate(self, generate: str | None, **kwargs) -> Optional[str]:
        """Run inference on the model."""
        pass

    def validate_output(self, output: Any) -> bool:
        return True

    def postprocessing(self, output: Any) -> Any:
        return output
