"""
paths.py -> Helps to build paths based on production and development environment configs.
"""

# ================== PROJECT ROOT =====================
import platform
import sys
import warnings
from pathlib import Path
from typing import Dict, Literal, Tuple

__ROOT__ = Path(__file__).absolute().resolve().parents[1]
sys.path.insert(0, str(__ROOT__))
from config import config

APP_ENVIRONMENT = config.CONFIG_TYPE
DEBUG = config.DEBUG

# ====================CORE_DIRS====================

ASSETS_DIR = __ROOT__ / "assets"
CONFIG_DIR = __ROOT__ / "config"
DB_DIR = __ROOT__ / "db"
ENV_DIR = __ROOT__ / "env"
VENV_DIR = __ROOT__ / "venvs"

# ===============FILE PATHS =======================

STORY_GRAMMARS_SCHEMA = __ROOT__ / "apps/story_teller/grammars/schema.gbnf"
SEARCH_QUERIES = __ROOT__ / "config/json/search_terms.json"
STORIES_JSON = __ROOT__ / "config/json/stories.json"

# ====================ASSETS SUB MAPS=====================

ASSETS_MAP = {
    "audio": ASSETS_DIR / "audio",
    "gifs": ASSETS_DIR / "gifs",
    "image": ASSETS_DIR / "image",
    "music": ASSETS_DIR / "music",
    "video": ASSETS_DIR / "video",
}


def ensure_dir(abs_path: str | Path):
    if isinstance(abs_path, str):
        abs_path = Path(abs_path)
    if not abs_path.is_dir():
        abs_path.mkdir(parents=True, exist_ok=True)


def ensure_files(abs_path: str | Path):
    if isinstance(abs_path, str):
        abs_path = Path(abs_path)
    if not abs_path.exists():
        abs_path.touch(exist_ok=True)


def get_python_venv(name: str, str_path: bool = False, debug: bool = DEBUG) -> str | Path | None:

    venv_path = VENV_DIR / name
    if not venv_path.exists():
        warnings.warn(f"Venv not found for {name}")
        return None
    system = platform.system()
    executables = {
        "Windows": venv_path / "Scripts/python.exe",
        "Darwin": venv_path / "bin/python",
        "Linux": venv_path / "bin/python",
    }
    if system not in executables:
        msg = f"Unsupported OS : {system}"
        if debug:
            raise OSError(msg)
        warnings.warn(msg)
        return None

    resolved = executables[system]
    return str(resolved) if str_path else resolved


def get_venv_mapping() -> Dict[str, Path | None]:
    AI_VENV_PATH = get_python_venv(name="ai_venv")
    SOCIAL_VENV_PATH = get_python_venv(name="social_venv")
    return {"ai": AI_VENV_PATH, "social": SOCIAL_VENV_PATH}


def check_all_assets_dir():
    for i in ASSETS_MAP.values():
        ensure_dir(abs_path=i)


LIST_OF_DIR = [ASSETS_DIR, CONFIG_DIR, DB_DIR, ENV_DIR, VENV_DIR]
LIST_OF_FILES = [STORY_GRAMMARS_SCHEMA, SEARCH_QUERIES]


def check_all_dir():
    for i in LIST_OF_DIR:
        ensure_dir(abs_path=i)


def check_all_files():
    for i in LIST_OF_FILES:
        ensure_files(abs_path=i)


check_all_dir()
check_all_files()
check_all_assets_dir()

for i in get_venv_mapping().values():
    if isinstance(i,str):
        print("s")
    else : print("P")
