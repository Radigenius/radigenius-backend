from abc import ABC, abstractmethod
from uuid import UUID
from typing import TypeVar, Type, Dict

from django.db.models.query import QuerySet
from django.http.request import HttpRequest


from domain.base import BaseModel


M = TypeVar("M", bound=BaseModel)


class IBaseHandler(ABC):

    view = None
    request: Type[HttpRequest]
    model: M
    schema = None

    @abstractmethod
    def __init__(self, view, request):
        pass

    @abstractmethod
    def check_object_permissions(self, obj):
        pass

    @abstractmethod
    def validate(self, data: dict):
        pass

    @abstractmethod
    def fetch_detail(self, *args, **kwargs) -> QuerySet:
        pass

    @abstractmethod
    def get_by_pk(self, pk: UUID) -> QuerySet:
        pass

    @abstractmethod
    def get_or_none(self, *args, **kwargs) -> QuerySet:
        pass

    @abstractmethod
    def get(self, *args, **kwargs) -> QuerySet:
        pass

    @abstractmethod
    def fetch_list(self) -> QuerySet:
        pass

    @abstractmethod
    def create(self, data: Dict) -> M:
        pass

    @abstractmethod
    def delete(self, *args, **kwargs) -> QuerySet:
        pass

    @abstractmethod
    def update(self, pk: UUID, data: Dict) -> QuerySet:
        pass

    @abstractmethod
    def partial_update(self, pk: UUID, data: Dict) -> QuerySet:
        pass

    @abstractmethod
    def get_list_for_current_user(self):
        raise NotImplementedError()
