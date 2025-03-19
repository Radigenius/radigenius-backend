from domain.apps.identity.models import User
from infrastructure.exceptions.exceptions import (
    UserIsNotActiveException,
    PasswordNotValidException,
)
from infrastructure.services.token import TokenService


class TokenCommand:
    @staticmethod
    def generate(data):

        password = data.get("password")
        email = data.get("email")

        token_service = TokenService()

        user = User.objects.get_by_email(email=email)

        if not user.is_active:
            raise UserIsNotActiveException()

        if (password and not user.check_password(password)):
            raise PasswordNotValidException()

        response = token_service.generate(user=user)

        return response

    @staticmethod
    def refresh(data):
        token_service = TokenService()
        decoded_token = token_service.decode(data.get("refresh"))
        user_id = decoded_token.get("user_id")
        user = User.objects.get(id=user_id)

        if not user.is_active:
            raise UserIsNotActiveException()

        return token_service.generate(user=user)
