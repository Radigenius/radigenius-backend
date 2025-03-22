from rest_framework.serializers import ModelSerializer, ChoiceField, UUIDField
from django.contrib.contenttypes.models import ContentType

from domain.apps.conversation.models import Message
from domain.apps.system.models import Attachment

class AttachmentModelSerializer(ModelSerializer):
    content_type = ChoiceField(
        choices=[
            ContentType.objects.get_for_model(Message).model
        ],
        required=True,
        write_only=True,
    )
    object_id = UUIDField(required=False, allow_null=True)

    class Meta:
        model = Attachment
        fields = [
            'id', 
            'file', 
            'content_type', 
            'object_id',
            'absolute_url', 
            'created_date',
        ]
        read_only_fields = ['id', 'absolute_url', 'created_date']