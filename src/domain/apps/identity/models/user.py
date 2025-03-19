from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from domain.apps.identity.managers import (
    UserManager,
    SuperUserManager,
    StaffUserManager,
    VIPUserManager,
    NormalUserManager
)
from domain.base import BaseModel

class User(BaseModel, AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(blank=True, unique=True)

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    last_used_ip = models.GenericIPAddressField(
        _("last used ip"), blank=True, null=True
    )

    objects = UserManager()
    super_users = SuperUserManager()
    staffs = StaffUserManager()
    vips = VIPUserManager()
    normals = NormalUserManager()

    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    is_vip = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    class Meta(BaseModel.Meta):
        pass

    def __str__(self):
        return self.email