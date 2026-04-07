from pathlib import Path

from dotenv import dotenv_values

from .dev import DevConfig
from .prod import ProdConfig

ROOT = Path(__file__).resolve().parents[2]
env_data = dotenv_values(ROOT / ".env")


def get_config():
    env = env_data.get("APP_ENV", "dev")
    if env == "prod":
        return ProdConfig()
    return DevConfig()
