from django.utils.translation import gettext_lazy as _

from .staff_user_manager import StaffUserManager
from infrastructure.exceptions.exceptions import ValidationException


class SuperUserManager(StaffUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_superuser=True)

    def create(self, **kwargs):

        if self.get_queryset().exists():
            raise ValidationException(message="Superuser is Already Created!")

        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_active", True)
        kwargs.setdefault("is_hidden", True)
        kwargs.setdefault("is_vip", True)
        kwargs.setdefault("is_verified", True)

        if not kwargs.get("is_superuser"):
            raise ValueError(_("Superuser must have is_superuser=True"))

        if not kwargs.get("is_hidden"):
            raise ValueError(_("Superuser must have is_hidden=True"))

        if not kwargs.get("is_vip"):
            raise ValueError(_("Superuser must have is_vip=True"))

        if not kwargs.get("is_active"):
            raise ValueError(_("Superuser must have is_active=True"))

        if not kwargs.get("is_staff"):
            raise ValueError(_("Superuser must have is_staff=True"))

        if not kwargs.get("is_verified"):
            raise ValueError(_("Superuser must have is_verified=True"))

        return super().create(**kwargs)
