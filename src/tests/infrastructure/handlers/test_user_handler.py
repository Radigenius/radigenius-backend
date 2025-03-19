import pytest
import factory

from django.utils import timezone

from domain.enums.identity.enum import BanReasons
from infrastructure.handlers.identity.user import UserHandler
from tests.base import BaseTest
from tests.factories.identity import UserFactory


@pytest.mark.django_db
class TestUserHandler(BaseTest):
    def test_get(self):
        # Arrange
        user = UserFactory()
        handler = UserHandler()

        # Act
        response = handler.get(id=user.id)

        # Assert
        assert str(response.id) == str(user.id)

    def test_get_by_pk(self):
        # Arrange
        user = UserFactory()
        handler = UserHandler()

        # Act
        response = handler.get_by_pk(pk=user.id)

        # Assert
        assert str(response.id) == str(user.id)

    def test_create(self):
        # Arrange
        user = factory.build(dict, FACTORY_CLASS=UserFactory)
        handler = UserHandler()

        # Act
        response = handler.create(user)

        # Assert
        assert response.phone_number == user.get("phone_number")

    def test_delete(self):
        # Arrange
        user = UserFactory()
        handler = UserHandler()

        # Act
        response = handler.delete(id=user.id)

        # Assert
        assert response[0] >= 1

    # def test_update(self):
    #     # Arrange
    #     user = factory.build(dict, FACTORY_CLASS=UserFactory)
    #     handler = UserHandler()
    #     dto = UserDto(**user)
    #
    #     # Act
    #     created = handler.create(dto=dto)
    #     dto.id = created.get("id")
    #     dto.phone_number = fake_phone_number_generator()
    #     response = handler.update(dto=dto)
    #
    #     # Assert
    #     assert response.get("phone_number") == dto.phone_number
    #     assert response.get("phone_number") != created.get("phone_number")

    def test_partial_update(self):
        # Arrange
        user = UserFactory()
        data = {"phone_number": "+989365411515"}

        # Act
        handler = UserHandler()
        response = handler.partial_update(user.id, data)

        # Assert
        assert response.phone_number == data.get("phone_number")
        assert response.phone_number != user.phone_number

    # def test_ban(self):
    #     # Arrange
    #     user = UserFactory()
    #     user_handler = UserHandler()

    #     # Act
    #     response = user_handler.ban(
    #         user_id=user.id, reason=BanReasons.ABUSIVE.value, until=timezone.now()
    #     )

    #     # Assert
    #     assert str(response.user.id) == str(user.id)

    # def test_unban(self):
    #     # Arrange
    #     user = UserFactory()
    #     user_handler = UserHandler()
    #     user_handler.ban(
    #         user_id=user.id,
    #         reason=BanReasons.ABUSIVE.value,
    #         until=timezone.now() + +timezone.timedelta(hours=2),
    #     )

    #     # Act
    #     response = user_handler.unban(user_id=user.id)

    #     assert response >= 1
