"""
paths.py -> 
"""

from app.config.loader import get_config

config = get_config()

assets = {
    "short": config.ASSETS_DIR / "videos/short"
}