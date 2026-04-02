



from pathlib import Path

__ROOT__ = Path(__file__).resolve().parents[2]

class BaseConfig:
    ASSETS_DIR = __ROOT__ / "assets"
    LLM_DIR = __ROOT__ / "models"