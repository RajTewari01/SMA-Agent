"""
base.py — Shared download infrastructure for all pipelines.

Responsibilities:
    1. User-Agent rotation pool
    2. Per-API header profiles (Pexels uses Authorization, Unsplash uses Client-ID, etc.)
    3. Secure API key loading from secrets.env.local
    4. Core HTTP helpers: fetch_json(), download_file()
"""

import random
import re
import unicodedata
import warnings
from pathlib import Path
from typing import Any, Dict, Optional

import requests
from dotenv import dotenv_values

# =========================================================
# PROJECT PATHS
# =========================================================

__ROOT__ = Path(__file__).resolve().absolute().parents[3]
_SECRETS_PATH = __ROOT__ / "env" / "secrets.env.local"

# =========================================================
# USER AGENT POOL — rotated per-request to reduce blocking
# =========================================================

_USER_AGENTS = [
    # Chrome on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    # Chrome on Mac
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    # Chrome on Linux
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
    # Firefox
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.3; rv:126.0) Gecko/20100101 Firefox/126.0",
    # Edge
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
    # Safari
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
    # Mobile
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36",
    # Brave / Vivaldi / Samsung
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Brave/125",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Vivaldi/6.5",
    # Older fallback
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
]

# =========================================================
# API KEY MAP — maps api_name to the env variable name
# in secrets.env.local
# =========================================================

_API_KEY_MAP: Dict[str, str] = {
    "Pexels": "Pixels_Image_Api_key",
    "Unsplash": "Unsplash_Api_Access_key",
    "Pixabay": "Pixabay_Api_key",
    "Giphy": "Giphy_Api_key",
}

# =========================================================
# PER-API HEADER PROFILES
# Each API authenticates differently:
#   - Pexels:     Authorization header with raw key
#   - Unsplash:   Authorization header with "Client-ID " prefix
#   - Pixabay:    URL param (no auth header needed)
#   - Giphy:      URL param (no auth header needed)
#   - DuckDuckGo: Referer-based, no API key
#   - yt-dlp:     Handled internally by yt-dlp
# =========================================================

def _build_pexels_headers(api_key: str) -> Dict[str, str]:
    return {"Authorization": api_key}


def _build_unsplash_headers(api_key: str) -> Dict[str, str]:
    return {"Authorization": f"Client-ID {api_key}"}


def _build_duckduckgo_headers(_: str = "") -> Dict[str, str]:
    return {
        "Referer": "https://duckduckgo.com/",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }


def _build_empty_headers(_: str = "") -> Dict[str, str]:
    """Pixabay, Giphy, and yt-dlp don't use auth headers."""
    return {}


_HEADER_BUILDERS = {
    "Pexels": _build_pexels_headers,
    "Unsplash": _build_unsplash_headers,
    "DuckDuckGo": _build_duckduckgo_headers,
    "Pixabay": _build_empty_headers,
    "Giphy": _build_empty_headers,
    "yt-dlp": _build_empty_headers,
}


# =========================================================
# BASE GATHERER CLASS
# =========================================================

class BaseGatherer:
    """
    Shared infrastructure for all download pipelines.

    Provides:
        - Search term sanitization
        - Secure API key loading
        - Per-API header generation
        - Core HTTP helpers (fetch_json, download_file)
    """

    _secrets_cache: Optional[Dict[str, str]] = None

    # --- Search Term Sanitization ---

    @staticmethod
    def sanitize_search_term(term: str) -> str:
        """Clean a search term: strip emojis, special chars, normalize."""
        if not term:
            return ""
        term = unicodedata.normalize("NFKD", term)
        term = term.encode("ascii", "ignore").decode("utf-8")
        term = re.sub(r"[-_.]", " ", term)
        term = re.sub(r"[^a-zA-Z0-9\s]", "", term)
        return re.sub(r"\s+", " ", term).strip().lower()

    # --- API Key Management ---

    @classmethod
    def _load_secrets(cls) -> Dict[str, str]:
        """Load secrets from env file, cached after first read."""
        if cls._secrets_cache is None:
            if _SECRETS_PATH.exists():
                cls._secrets_cache = dotenv_values(_SECRETS_PATH)
            else:
                warnings.warn(f"Secrets file not found: {_SECRETS_PATH}")
                cls._secrets_cache = {}
        return cls._secrets_cache

    @classmethod
    def load_api_key(cls, api_name: str) -> Optional[str]:
        """
        Securely load an API key for a given API name.

        Args:
            api_name: One of 'Pexels', 'Unsplash', 'Pixabay', 'Giphy'.

        Returns:
            The API key string, or None if not found.
        """
        env_var = _API_KEY_MAP.get(api_name)
        if not env_var:
            return None
        secrets = cls._load_secrets()
        key = secrets.get(env_var)
        if not key:
            warnings.warn(f"API key '{env_var}' not found in {_SECRETS_PATH.name}")
        return key

    # --- Header Generation ---

    @classmethod
    def get_headers(cls, api_name: str) -> Dict[str, str]:
        """
        Build the complete headers dict for an API request.

        Includes a random User-Agent plus the API-specific auth headers
        (e.g. Authorization for Pexels, Client-ID for Unsplash).

        Args:
            api_name: The api_name from ConfigPipeline (e.g. 'Pexels', 'Unsplash').

        Returns:
            A headers dictionary ready for requests.get().
        """
        headers = {"User-Agent": random.choice(_USER_AGENTS)}

        builder = _HEADER_BUILDERS.get(api_name, _build_empty_headers)
        api_key = cls.load_api_key(api_name) or ""
        api_headers = builder(api_key)
        headers.update(api_headers)

        return headers

    # --- HTTP Helpers ---

    @staticmethod
    def fetch_json(
        url: str,
        headers: Dict[str, str],
        params: Optional[Dict[str, Any]] = None,
        timeout: tuple = (6, 30),
    ) -> Optional[Dict]:
        """
        Make a GET request and return parsed JSON.

        Returns None on failure instead of raising.
        """
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=timeout)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            warnings.warn(f"API request failed [{url}]: {e}")
            return None

    @staticmethod
    def download_file(
        url: str,
        dest: Path,
        headers: Optional[Dict[str, str]] = None,
        timeout: tuple = (6, 60),
        chunk_size: int = 8192,
    ) -> bool:
        """
        Stream-download a file to disk.

        Args:
            url: Direct download URL.
            dest: Destination file path.
            headers: Optional request headers.
            timeout: (connect, read) timeout tuple.
            chunk_size: Bytes per chunk.

        Returns:
            True on success, False on failure.
        """
        dl_headers = headers or {"User-Agent": random.choice(_USER_AGENTS)}
        try:
            resp = requests.get(url, headers=dl_headers, stream=True, timeout=timeout)
            resp.raise_for_status()
            with open(dest, "wb") as f:
                for chunk in resp.iter_content(chunk_size):
                    if chunk:
                        f.write(chunk)
            return True
        except requests.RequestException as e:
            warnings.warn(f"Download failed [{url}]: {e}")
            return False
