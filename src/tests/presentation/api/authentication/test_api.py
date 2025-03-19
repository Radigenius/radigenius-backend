import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

# from domain.apps.identity.managers import SECURE_OTP_CODE
from infrastructure.exceptions.exceptions import UserIsNotActiveException
from infrastructure.services.token import TokenService
from tests.factories.identity import (
    UserFactory,
    fake_email_generator,
)
from tests.base import BaseTest

User = get_user_model()


@pytest.mark.django_db
class TestAuthenticationAPI(BaseTest):
    def test_generate_token_for_not_active_user(self):
        # Arrange
        endpoint = reverse("jwt-generate")
        password = "@123456!"
        email = fake_email_generator()
        user = User.objects.create(
            password=password,
            email=email,
            is_active=False,
        )

        # Act
        response = self.api_client.post(
            endpoint, data={"email": email, "password": password}
        )

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get("key") == UserIsNotActiveException().key

    def test_generate_token_for_active_user(self):
        # Arrange
        endpoint = reverse("jwt-generate")
        password = "@123456!"
        email = fake_email_generator()
        user = User.objects.create(
            password=password,
            email=email,
            is_active=True,
        )

        # Act
        response = self.api_client.post(
            endpoint, data={"email": email, "password": password}
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("data").get("access_token", "") != ""
        assert response.data.get("data").get("refresh_token", "") != ""
        # assert response.data.get("data").get("profile", "") != ""

    # def test_generate_token_for_active_user_with_otp(self):
    #     # Arrange
    #     endpoint = reverse("jwt-generate")
    #     email = fake_email_generator()
    #     user = UserFactory(is_active=True, email=email)

    #     # Act
    #     response = self.api_client.post(
    #             endpoint, data={"phone_number": phone_number, "otp": SECURE_OTP_CODE}
    #     )

    #     # Assert
    #     assert response.status_code == status.HTTP_200_OK
    #     assert response.data.get("data").get("access_token", "") != ""
    #     assert response.data.get("data").get("refresh_token", "") != ""
    #     # assert response.data.get("data").get("profile", "") != ""

    def test_refresh_token_for_not_active_user(self):
        # Arrange
        endpoint = reverse("jwt-refresh")
        password = "@123456!"
        email = fake_email_generator()
        user = UserFactory(
            is_active=False, email=email, password=password
        )

        token_service = TokenService()
        token = token_service.generate(user)

        # Act
        response = self.api_client.post(
            endpoint, data={"refresh": token.get("refresh_token")}
        )

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get("key") == UserIsNotActiveException().key

    def test_refresh_token_for_active_user(self):
        # Arrange
        endpoint = reverse("jwt-refresh")
        password = "@123456!"
        email = fake_email_generator()
        user = UserFactory(is_active=True, email=email, password=password)

        token_service = TokenService()
        token = token_service.generate(user)

        # Act
        response = self.api_client.post(
            endpoint, data={"refresh": token.get("refresh_token")}
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("data").get("access_token", "") != ""
        assert response.data.get("data").get("refresh_token", "") != ""
