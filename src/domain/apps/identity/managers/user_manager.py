from domain.base import BaseManager
from django.contrib.auth.models import BaseUserManager

from infrastructure.exceptions.exceptions import ValidationException


class UserManager(BaseUserManager, BaseManager):
    def prepare_list_queryset(self):
        return super().prepare_list_queryset().filter(is_hidden=False)

    def get_by_email(self, email: str):
        return self.initialize_queryset().get_or_not_found_exception(
            email=email
        )

    def create(self, **kwargs):

        password = kwargs.pop("password", None)

        if not password:
            raise ValidationException(message="Password Must be Set!")

        user = self.model(**kwargs)
        user.set_password(password)
        user.save()
        return user
