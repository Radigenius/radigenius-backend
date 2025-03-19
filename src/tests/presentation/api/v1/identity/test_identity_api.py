import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

# from domain.apps.identity.managers import SECURE_OTP_CODE
# from domain.apps.identity.models import OTP
from infrastructure.exceptions.exceptions import (
    InvalidOTPException,
    EntityNotFoundException,
)
from tests.factories.identity import (
    UserFactory,
)
from tests.base import BaseTest

User = get_user_model()


@pytest.mark.django_db
class TestIdentityAPI(BaseTest):
    def test_user_create(self):
        # Arrange
        endpoint = reverse("users-list")
        request = {
            "email": "test@test.com",
            "password": "@123456!",
            "otp": SECURE_OTP_CODE,
        }

        # Act
        response = self.api_client.post(endpoint, data=request)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED

        assert response.data.get("data").get("access_token", "") != ""
        assert response.data.get("data").get("refresh_token", "") != ""
        # assert response.data.get("data").get("profile").get("user").get(
        #     "phone_number", ""
        # ) == request.get("phone_number")
        # assert (
        #     response.data.get("data")
        #     .get("profile")
        #     .get("user")
        #     .get("is_verified", False)
        #     == True
        # )

    # def test_verify_otp_true(self):
    #     # Arrange
    #     endpoint = reverse("users-verify-otp")
    #     phone_number = "+989365411515"

    #     otp, created = OTP.objects.get_or_create(phone_number=phone_number)
    #     request = {"phone_number": phone_number, "otp": otp.code}

    #     # Act
    #     response = self.api_client.post(endpoint, data=request)

    #     # Assert
    #     assert response.status_code == status.HTTP_200_OK
    #     assert response.data.get("data") == True

    # def test_verify_otp_false(self):
    #     # Arrange
    #     endpoint = reverse("users-verify-otp")
    #     phone_number = "+989365411515"

    #     otp = OTP.objects.get_or_create(phone_number=phone_number)
    #     request = {"phone_number": phone_number, "otp": "1234"}

    #     # Act
    #     response = self.api_client.post(endpoint, data=request)

    #     # Assert
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     assert response.data.get("key") == InvalidOTPException().key
    #     assert response.data.get("data") == None

    # def test_generate_otp(self):
    #     # Arrange
    #     endpoint = reverse("users-generate-otp")
    #     phone_number = fake_phone_number_generator()
    #     user = UserFactory(phone_number=phone_number)
    #     payload = {
    #         "phone_number": phone_number,
    #         "template": SMSTemplates.OTPLogin,
    #     }

    #     # Act
    #     response = self.api_client.post(endpoint, data=payload)

    #     # Assert
    #     assert response.status_code == status.HTTP_200_OK
