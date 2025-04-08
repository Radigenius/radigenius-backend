from rest_framework.permissions import AllowAny
from rest_framework.decorators import action

from application.permissions.permissions import (
    CurrentUserOrAdmin,
    IsAdminUser,
    IsAuthenticated,
)
from application.enums.throttle.enums import ThrottleScopes
from infrastructure.commands.identity.user import UserCommand
from infrastructure.serializers.identity import (
    UserModelSerializer,
    UserRegisterSerializer,
    UserResetPasswordSerializer,
    UserChangePasswordSerializer,
    EmailSerializer,
    OTPGenerateSerializer,
    OTPVerifySerializer,
)
from presentation.controllers.base import CustomGenericViewSet


class IdentityModelViewSet(CustomGenericViewSet):
    throttle_scope = ThrottleScopes.High.value
    output_serializer_class = UserModelSerializer
    command_class = UserCommand
    permission_classes = [IsAdminUser]

    def set_input_serializer_class(self):
        if self.action == "create":
            self.input_serializer_class = UserRegisterSerializer
        # if self.action == "reset_password":
        #     self.input_serializer_class = UserResetPasswordSerializer
        if self.action == "generate_otp":
            self.input_serializer_class = OTPGenerateSerializer
        # if self.action == "change_password":
        #     self.input_serializer_class = UserChangePasswordSerializer
        if self.action in ["get_by_email", "get_by_email_or_none"]:
            self.input_serializer_class = EmailSerializer
        if self.action == "verify_otp":
            self.input_serializer_class = OTPVerifySerializer

    def get_permissions(self):
        if (self.action in ["create", "get_by_email", "get_by_email_or_none", "generate_otp", "verify_otp"]):
            self.permission_classes = [AllowAny]
        if self.action == "retrieve":
            self.permission_classes = [CurrentUserOrAdmin]
        if self.action == "change_password":
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        return self.command_class(self, request).retrieve(request.data)

    def list(self, request, *args, **kwargs):
        return self.command_class(self, request).list(paginated=True)

    def create(self, request, *args, **kwargs):
        return self.command_class(self, request).create(request.data)

    @action(["post"], detail=False)
    def generate_otp(self, request, *args, **kwargs):
        return self.command_class(self, request).generate_otp(request.data)

    @action(["post"], detail=False)
    def get_by_email(self, request, *args, **kwargs):
        return self.command_class(self, request).get_by_email(request.data)

    @action(["post"], detail=False)
    def get_by_email_or_none(self, request, *args, **kwargs):
        return self.command_class(self, request).get_by_email_or_none(request.data)

    @action(["post"], detail=False)
    def verify_otp(self, request, *args, **kwargs):
        return self.command_class(self, request).verify_OTP(request.data)
