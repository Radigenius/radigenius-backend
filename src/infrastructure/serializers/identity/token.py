from rest_framework.serializers import (
    Serializer,
    CharField,
)
from decouple import config

from .email import EmailSerializer

TEST_ENV = config("TEST_ENV", cast=bool, default=False)

class TokenObtainPairSerializer(EmailSerializer):
    password = CharField()


class TokenRefreshSerializer(Serializer):
    refresh = CharField()
