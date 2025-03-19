from typing import TypeVar, Any

from django.core.exceptions import ValidationError
from django.db import models

from domain.base import CustomQuerySet
from infrastructure.exceptions.exceptions import (
    ValidationException,
)

T = TypeVar("T", bound=models.Model)


class CustomManager(models.Manager):
    def get_queryset(self):
        return CustomQuerySet(self.model, using=self._db)

    def all_objects(self) -> "models.QuerySet[T]":
        """
        Return a queryset of all objects, including those filtered in 'get_queryset'.
        """
        return super().get_queryset()

    def initialize_queryset(self, queryset=None):
        """
        Initialize the base queryset that all other queries should build upon.
        """
        return queryset if queryset is not None else self.get_queryset()

    def prepare_list_queryset(self, queryset=None):
        """
        Prepare a queryset for list views, building upon the initialized queryset.
        """
        return self.initialize_queryset(queryset)

    def prepare_detail_queryset(self, queryset=None):
        """
        Prepare a queryset for retrieving a single object in detail, building upon the initialized queryset.
        """
        return self.initialize_queryset(queryset)

    def fetch_list(self):
        """
        Fetch a list of objects using the prepared list queryset.
        """
        return self.prepare_list_queryset()

    def fetch_detail(self, *args, **kwargs) -> T:
        """
        Fetch a single object in detail using the prepared detail queryset.
        """
        return self.prepare_detail_queryset().get_or_not_found_exception(
            *args, **kwargs
        )

    def partial_update(self, id, **kwargs) -> T:
        """
        Partially update an object. Raise EntityNotFoundException if not found.
        """
        try:
            instance = self.get_queryset().get_or_not_found_exception(id=id)
            updated_fields = []

            for attr, value in kwargs.items():
                if hasattr(instance, attr):
                    setattr(instance, attr, value)
                    updated_fields.append(attr)

            instance.full_clean()
            instance.save(update_fields=updated_fields)
            return instance
        except ValidationError as e:
            raise ValidationException(errors=e)


class BaseManager(CustomManager.from_queryset(CustomQuerySet)):
    pass
