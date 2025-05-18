from rest_framework.permissions import AllowAny
from rest_framework.decorators import action

from application.permissions.permissions import (
    CurrentUserOrAdmin,
    IsAdminUser,
    IsAuthenticated,
)
from application.enums.throttle.enums import ThrottleScopes
from infrastructure.commands.conversation.chat import ChatCommand
from presentation.controllers.base import CustomGenericViewSet

from infrastructure.serializers.conversation import ChatModelSerializer, ChatSmallModelSerializer , ChatCreateSerializer, MessageCreateSerializer, MessageModelSerializer

class ConversationGenericViewSet(CustomGenericViewSet):
    throttle_scope = ThrottleScopes.High.value
    input_serializer_class = ChatCreateSerializer
    output_serializer_class = ChatSmallModelSerializer
    command_class = ChatCommand
    permission_classes = [IsAuthenticated]

    def set_input_serializer_class(self):
        if self.action == "send_message":
            self.input_serializer_class = MessageCreateSerializer

    def set_output_serializer_class(self):

        if self.action in ["retrieve"]:
            self.output_serializer_class = ChatModelSerializer

        if self.action == "send_message":
            self.output_serializer_class = MessageModelSerializer

    def get_permissions(self):
        if self.action in ["get_list_for_current_user", "retrieve"]:
            self.permission_classes = [CurrentUserOrAdmin]
        if self.action == "list":
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def retrieve(self, request, pk=None):
        return self.command_class(self, request).retrieve(pk=pk)

    def list(self, request, *args, **kwargs):
        return self.command_class(self, request).list(paginated=True)

    def create(self, request, *args, **kwargs):
        return self.command_class(self, request).create(request.data)
    
    @action(["get"], detail=False)
    def get_list_for_current_user(self, request):
        return self.command_class(self, request).get_list_for_current_user(
            paginated=False
        )
    
    @action(["post"], detail=True)
    def send_message(self, request, *args, **kwargs):
        return self.command_class(self, request).send_message(chat_id=kwargs.get("pk"), message=request.data)