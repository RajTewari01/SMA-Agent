from pathlib import Path

__ROOT__ = Path(__file__).resolve().parents[1]

class BaseConfig:
    ASSETS_DIR = __ROOT__ / "assets"
    LLM_DIR = __ROOT__ / "models"
    D_EXEC = False
    IMMEDIATE_EXEC = False
    IMMEDIATE_ERROR_VALIDATION = True