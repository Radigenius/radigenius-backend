from functools import wraps

from application.enums.services.enum import CacheKeys
from infrastructure.services.cache import CacheService


def with_cached_result(cache_key: CacheKeys):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            cached_result = CacheService.get(cache_key.key)

            if cached_result is not None:
                return cached_result

            result = func(*args, **kwargs)

            if result is not None:
                CacheService.set(cache_key.key, result, cache_key.ttl)

            return result

        return wrapper

    return decorator
