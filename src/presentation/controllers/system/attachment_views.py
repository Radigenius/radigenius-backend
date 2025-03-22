from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from infrastructure.commands.system.attachment import AttachmentCommand
from infrastructure.serializers.system import (
    AttachmentModelSerializer, 
)
from presentation.controllers.base import CustomGenericViewSet


class AttachmentGenericViewSet(CustomGenericViewSet):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    input_serializer_class = AttachmentModelSerializer
    output_serializer_class = AttachmentModelSerializer
    command = AttachmentCommand
    
    def create(self, request, *args, **kwargs):
        command = self.command(self, request)
        return command.create(request.data)
    
    def destroy(self, request, *args, **kwargs):
        command = self.command(self, request)
        return command.destroy(pk=kwargs.get("pk"))
