from datetime import timedelta
from typing import Callable, Any
from cachetools import TTLCache
from functools import wraps

# Create a cache with a maximum size and 5-minute TTL
cache_store = TTLCache(maxsize=100, ttl=timedelta(minutes=5).total_seconds())

def cache(ttl: int = 300):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            # Create a cache key based on function name and arguments
            cache_key = (func.__name__, str(args), str(kwargs))
            
            # Try to get result from cache
            if cache_key in cache_store:
                return cache_store[cache_key]
                
            # If not in cache, call the function and store the result
            result = await func(*args, **kwargs)
            cache_store[cache_key] = result
            return result
        return wrapper
    return decorator