from django.db import models
from django.utils import timezone
from domain.base import BaseModel
from domain.apps.identity.managers import OTPManager


class OTP(BaseModel):
    code = models.IntegerField()
    email = models.EmailField()
    until = models.DateTimeField()

    objects = OTPManager()

    class Meta(BaseModel.Meta):
        pass

    @property
    def is_active(self):
        return self.until >= timezone.now()

    def __str__(self):
        return str(self.code)
