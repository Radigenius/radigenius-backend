from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView

from application.enums.throttle.enums import ThrottleScopes
from infrastructure.commands.identity.token import TokenCommand
from infrastructure.serializers.identity import (
    TokenRefreshSerializer,
    TokenObtainPairSerializer,
)


class CustomTokenObtainPairView(GenericAPIView):
    throttle_scope = ThrottleScopes.High.value
    serializer_class = TokenObtainPairSerializer
    command = TokenCommand

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        command = self.command()
        response = command.generate(serializer.validated_data)

        return Response(data={"data": response}, status=status.HTTP_200_OK)


class CustomTokenRefreshView(GenericAPIView):
    throttle_scope = ThrottleScopes.High.value
    serializer_class = TokenRefreshSerializer
    command = TokenCommand

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        command = self.command()
        response = command.refresh(serializer.validated_data)

        return Response(data={"data": response}, status=status.HTTP_200_OK)
