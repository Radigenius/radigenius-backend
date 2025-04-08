from rest_framework.serializers import ChoiceField, Serializer, IntegerField
from infrastructure.serializers.identity.email import EmailSerializer
from application.enums.services.enum import EmailTemplates

from decouple import config


class OTPGenerateSerializer(EmailSerializer):
    template = ChoiceField(
        choices=[
            EmailTemplates.OTPRegister,
        ],
        required=True,
    )


TEST_ENV = config("TEST_ENV", cast=bool, default=False)

class OTPFieldSerializer(Serializer):
    otp = IntegerField(min_value=1_000, max_value=999_999 if TEST_ENV else 9999, required=True)

class OTPVerifySerializer(EmailSerializer, OTPFieldSerializer):
    pass
