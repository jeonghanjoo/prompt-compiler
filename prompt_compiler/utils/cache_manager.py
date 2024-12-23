import json
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime, timedelta


class CacheManager:
    """Manages caching of AI responses."""

    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_key(self, prompt_data: Dict[str, Any]) -> str:
        """Generate a unique cache key for the prompt data."""
        # Sort dictionary to ensure consistent hashing
        sorted_data = json.dumps(prompt_data, sort_keys=True)
        return hashlib.sha256(sorted_data.encode()).hexdigest()

    def get_cached_response(self, prompt_data: Dict[str, Any]) -> Optional[str]:
        """Get cached response if it exists and is valid."""
        cache_key = self._get_cache_key(prompt_data)
        cache_file = self.cache_dir / f"{cache_key}.json"

        if not cache_file.exists():
            return None

        try:
            with open(cache_file, "r") as f:
                cache_data = json.load(f)

            # Check if cache is expired (default: 24 hours)
            cached_time = datetime.fromisoformat(cache_data["timestamp"])
            if datetime.now() - cached_time > timedelta(hours=24):
                return None

            return cache_data["response"]
        except (json.JSONDecodeError, KeyError, ValueError):
            return None

    def cache_response(self, prompt_data: Dict[str, Any], response: str) -> None:
        """Cache the AI response."""
        cache_key = self._get_cache_key(prompt_data)
        cache_file = self.cache_dir / f"{cache_key}.json"

        cache_data = {
            "timestamp": datetime.now().isoformat(),
            "prompt_data": prompt_data,
            "response": response,
        }

        with open(cache_file, "w") as f:
            json.dump(cache_data, f, indent=2)
