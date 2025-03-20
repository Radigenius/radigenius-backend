from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.response import Response

from infrastructure.commands.base import BaseCommand
from infrastructure.handlers.system.attachment import AttachmentHandler

class AttachmentCommand(BaseCommand):
    handler = AttachmentHandler

    def create(self, data):

        validated_data = self.validate(data)
        
        # Convert the content_type model name to an actual ContentType instance
        content_type = ContentType.objects.get(model=validated_data['content_type'])
        validated_data['content_type'] = content_type

        queryset = self._prepare_handler().create(validated_data)
        serializer = self.view.get_output_serializer(queryset)

        return Response(data={"data": serializer.data}, status=status.HTTP_201_CREATED)