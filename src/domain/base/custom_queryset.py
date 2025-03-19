from uuid import uuid4 as GUID
from typing import TypeVar, Any, Optional

from django.db import models

from infrastructure.exceptions.exceptions import (
    MultipleObjectsReturnedException,
    EntityNotFoundException,
)

T = TypeVar("T", bound=models.Model)


class CustomQuerySet(models.QuerySet):
    def get_or_not_found_exception(self, *args, **kwargs):
        """
        Perform a get() query but raise NotFoundException if not found.
        """
        try:
            return self.get(*args, **kwargs)
        except self.model.DoesNotExist:
            raise EntityNotFoundException(
                f"{self.model.__name__} Not Found!",
                errors=[{"args": args, "kwargs": kwargs}],
            )
        except self.model.MultipleObjectsReturned:
            raise MultipleObjectsReturnedException(
                message=f"Multiple {self.model.__name__} objects returned."
            )

    def get_or_none(self, *args, **kwargs) -> Optional[T]:
        """
        Perform a get() query but return None if the object is not found instead of raising an exception.
        """
        try:
            return self.get(*args, **kwargs)
        except self.model.DoesNotExist:
            return None
