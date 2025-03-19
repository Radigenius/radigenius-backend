from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    CharField,
    SerializerMethodField,
)
from rest_framework.validators import UniqueTogetherValidator

from domain.apps.identity.models import User

from infrastructure.validators.identity.serializer_validators import (
    PasswordValidator,
)
from .email import EmailSerializer


class UserModelSerializer(ModelSerializer):
    # has_password = SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "date_joined",
            "is_active",
            "is_verified",
            "is_superuser",
            "is_staff",
            "is_hidden",
            "is_vip",
            # "has_password",
            "created_date",
        ]
        read_only_fields = [
            "id",
            "username",
            "date_joined",
            "is_active",
            "is_verified",
            "is_superuser",
            "is_staff",
            "is_hidden",
            "is_vip",
            # "has_password",
            "created_date",
        ]

class UserRegisterSerializer(EmailSerializer):
    password = CharField(required=True)

    class Meta:
        validators = EmailSerializer.Meta.validators + [
            PasswordValidator(field_name="password")
        ]


class UserResetPasswordSerializer(EmailSerializer):
    password = CharField()

    class Meta:
        validators = EmailSerializer.Meta.validators + [
            PasswordValidator(field_name="password")
        ]


class UserChangePasswordSerializer(Serializer):
    old_password = CharField(required=True)
    password = CharField(required=True)

    class Meta:
        validators = [PasswordValidator(field_name="password")]
