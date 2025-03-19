from typing import Type, Dict, Union
from abc import ABC, abstractmethod
from uuid import UUID

from django.http.request import HttpRequest

from application.interfaces.handlers.base import IBaseHandler
from presentation.controllers.base import CustomGenericAPIView, CustomGenericViewSet


class IBaseCommand(ABC):
    handler: Type[IBaseHandler]
    view: Union[CustomGenericAPIView, CustomGenericViewSet]
    request: HttpRequest

    @abstractmethod
    def _filter_queryset(self, queryset):
        pass

    @abstractmethod
    def _paginate_queryset(self, queryset):
        pass

    @abstractmethod
    def _prepare_handler(self):
        pass

    @abstractmethod
    def list(self, paginated: bool):
        pass

    @abstractmethod
    def create(self, data: Dict):
        pass

    @abstractmethod
    def retrieve(self, *args):
        pass

    @abstractmethod
    def update(self, pk: UUID, data):
        pass

    @abstractmethod
    def partial_update(self, pk: UUID, data: dict):
        pass

    @abstractmethod
    def destroy(self, pk):
        pass
