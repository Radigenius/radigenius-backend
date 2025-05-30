from abc import ABC, abstractmethod
from django.db.models import Model

from application.dtos.base import BaseDto


class IDtoService(ABC):

    @abstractmethod
    def asdict(self, dto) -> dict:
        pass

    @abstractmethod
    def cast(self, data: dict, dto) -> BaseDto:
        pass

    @abstractmethod
    def cast_from_model(self, model: Model, dto):
        pass