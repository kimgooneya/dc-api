from datetime import datetime, timedelta
import hashlib
from typing import Dict, Tuple, Any

class SimpleCache:
    def __init__(self, cache_duration: timedelta):
        self.cache: Dict[str, Tuple[Any, datetime]] = {}
        self.cache_duration = cache_duration
    
    def get(self, key: str) -> Any:
        """Get a value from the cache if it exists and is not expired"""
        if key in self.cache:
            value, timestamp = self.cache[key]
            if datetime.now() - timestamp < self.cache_duration:
                return value
            # Remove expired entry
            del self.cache[key]
        return None
    
    def set(self, key: str, value: Any) -> None:
        """Set a value in the cache with current timestamp"""
        self.cache[key] = (value, datetime.now())
    
    def generate_key(self, *args, **kwargs) -> str:
        """Generate a cache key from arguments"""
        # Create a string representation of args and kwargs
        key_content = str(args) + str(sorted(kwargs.items()))
        # Create MD5 hash of the key content
        return hashlib.md5(key_content.encode()).hexdigest()
    
    def clear(self) -> None:
        """Clear all cache entries"""
        self.cache.clear() 