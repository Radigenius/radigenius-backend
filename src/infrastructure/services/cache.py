from django.core.cache import cache
from decouple import config

from application.interfaces.services.cache import ICacheService


class CacheService(ICacheService):
    @classmethod
    def delete(cls, key: str):
        if config("TEST_ENV", cast=bool, default=False):
            cache.delete(key)
        else:
            cache.delete_pattern(f"*{key}*")

    @classmethod
    def get(cls, key: str):
        return cache.get(key)

    @classmethod
    def set(cls, key: str, data, timeout: int):
        cache.set(key, data, timeout)
