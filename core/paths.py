"""
paths.py -> Helps to build paths based on production and development environment configs.

NOTE : Still contains all the paths for the local devs
"""

from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path

from config import config

__ROOT__ = Path(__file__).resolve().absolute().parents[1]

class PathType(Enum):
    DEVPATH = auto()
    PRODPATH = auto()


@dataclass
class PathConfig:
    path_type: PathType
    base_path: str


downloaded_assets = {
    "audio" : Path(__ROOT__ / "assets/audio"),
    "video" : Path(__ROOT__ / "assets/video"),
    "image" : Path(__ROOT__ / "assets/image"),
    "gifs" : Path(__ROOT__ / "assets/gifs"),
    "music" : Path(__ROOT__ / "assets/music"),
    "song" : Path(__ROOT__ / "assets/song"),
}

SEARCH_QUERIES = Path(__ROOT__ / "config/json/search_terms.json")

