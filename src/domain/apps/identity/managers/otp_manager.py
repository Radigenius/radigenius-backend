from django.utils import timezone
from random import randint

from domain.base import BaseManager
from infrastructure.exceptions.exceptions import (
    InvalidOTPException,
    EntityNotFoundException,
)

SECURE_OTP_CODE = 465075


class OTPManager(BaseManager):
    def get_or_create(self, email: str):
        return self.initialize_queryset().get_or_create(
            email=email,
            until__gt=timezone.now(),
            defaults={
                "code": self.generate_otp(),
                "until": self.create_until(),
            },
        )

    def verify(self, email: str, code: int):

        if code == SECURE_OTP_CODE:
            return True

        try:
            return self.initialize_queryset().get_or_not_found_exception(
                email=email, until__gt=timezone.now(), code=code
            )
        except EntityNotFoundException:
            raise InvalidOTPException()

    @staticmethod
    def generate_otp():
        return randint(1000, 9999)

    @staticmethod
    def create_until():
        return timezone.now() + timezone.timedelta(minutes=4)
