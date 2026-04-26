from cachetools import TTLCache
from typing import Any, Optional

class CacheManager:
    """
    Abstraction layer for caching. Currently uses In-Memory cachetools.
    Can be swapped to Redis by updating these methods.
    """
    def __init__(self, maxsize: int = 1000, ttl: int = 3600):
        # Default 1 hour TTL
        self._cache = TTLCache(maxsize=maxsize, ttl=ttl)
        
    async def get(self, key: str) -> Optional[Any]:
        return self._cache.get(key)
        
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        # Note: cachetools TTLCache handles TTL globally per cache instance.
        # For a true Redis swap with per-key TTL, we abstract it here.
        self._cache[key] = value
        
    async def delete(self, key: str) -> None:
        if key in self._cache:
            del self._cache[key]

# Singleton instance
cache_manager = CacheManager()
