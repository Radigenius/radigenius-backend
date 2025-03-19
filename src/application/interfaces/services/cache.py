from abc import ABC, abstractmethod


class ICacheService(ABC):

    @classmethod
    @abstractmethod
    def delete(cls, key: str):
        pass

    @classmethod
    @abstractmethod
    def get(cls, key: str):
        pass

    @classmethod
    @abstractmethod
    def set(cls, key: str, data, timeout: int):
        pass