from django.utils import timezone
from django.conf import settings
from django.db.models import QuerySet, Q
from rest_framework_simplejwt.tokens import RefreshToken
import jwt

from domain.apps.identity.models import User
from application.interfaces.services.token import ITokenService
from infrastructure.exceptions.exceptions import InvalidTokenException
from infrastructure.serializers.identity.user import UserModelSerializer

class TokenService(ITokenService):
    def decode(self, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                settings.SECRET_KEY,
                settings.SIMPLE_JWT.get("algorithm") or "HS256",
            )
        except Exception as e:
            raise InvalidTokenException()

    def generate(self, user: User | QuerySet) -> dict:
        refresh = RefreshToken.for_user(user)

        User.objects.filter(id=user.id).update(last_login=timezone.now())

        return {
            "refresh_token": str(refresh),
            "access_token": str(refresh.access_token),
            "user": UserModelSerializer(user).data
        }
