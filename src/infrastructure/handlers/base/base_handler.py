from uuid import UUID
from typing import Generic, TypeVar, Dict

from django.core.exceptions import ImproperlyConfigured
from django.db.models.query import QuerySet

from application.interfaces.handlers.base import IBaseHandler
from domain.base import BaseModel
from infrastructure.exceptions.exceptions import (
    ValidationException,
    EntityNotFoundException,
    MultipleObjectsReturnedException,
)
from infrastructure.validators.base import Validator


M = TypeVar("M", bound=BaseModel)


class BaseHandler(Generic[M], IBaseHandler):

    schema = None

    def __init__(self, view=None, request=None):

        if not self.model or not issubclass(self.model, BaseModel):
            raise ImproperlyConfigured("Handlers Should define a model Property!")

        self.view = view
        self.request = request

    def check_object_permissions(self, obj: M):
        if (
            self.view is not None
            and obj is not None
            and hasattr(self.view, "check_object_permissions")
            and callable(getattr(self.view, "check_object_permissions"))
        ):
            self.view.check_object_permissions(self.request, obj)

    def validate(self, data: dict):

        if self.schema and not Validator.validate(data, self.schema):
            raise ValidationException(errors=Validator.errors)

        return data

    def fetch_detail(self, *args, **kwargs) -> M:
        result = self.model.objects.fetch_detail(*args, **kwargs)
        self.check_object_permissions(result)
        return result

    def get_or_none(self, *args, **kwargs) -> M:
        result = self.model.objects.get_or_none(*args, **kwargs)
        self.check_object_permissions(result)
        return result

    def get(self, *args, **kwargs) -> M:
        queryset = self.model.objects.get_or_not_found_exception(*args, **kwargs)
        self.check_object_permissions(queryset)
        return queryset

    def get_by_pk(self, pk: UUID) -> M:
        return self.get(pk=pk)

    def fetch_list(self) -> QuerySet:
        result = self.model.objects.fetch_list()
        self.check_object_permissions(result)
        return result

    def create(self, data: Dict) -> M:
        validated_data = self.validate(data)
        return self.model.objects.create(**validated_data)

    def delete(self, *args, **kwargs) -> QuerySet:
        return self.model.objects.filter(*args, **kwargs).delete()

    def update(self, pk, data: Dict) -> M:

        if not pk:
            raise ValidationException(errors={"id": "Id Is Required"})

        validated_data = self.validate(data)
        queryset = self.model.objects.filter(id=pk)
        count = queryset.count()

        if count == 0:
            raise EntityNotFoundException(f"{self.model.__name__} Not Found!")

        if count > 1:
            raise MultipleObjectsReturnedException(
                message=f"Multiple {self.model.__name__} objects returned."
            )

        queryset.update(**validated_data)
        return queryset.first()

    def partial_update(self, pk: UUID, data: Dict) -> M:
        return self.update(pk, data)

    def get_list_for_current_user(self):
        raise NotImplementedError()
