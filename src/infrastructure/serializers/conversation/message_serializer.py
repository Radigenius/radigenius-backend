from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    CharField,
    UUIDField,
    ListField,
    SerializerMethodField,
)
from domain.apps.conversation.models import Message
from infrastructure.validators.identity.serializer_validators import (
    EitherFieldRequired,
)
from infrastructure.serializers.system.attachment_serializer import AttachmentModelSerializer

class MessageModelSerializer(ModelSerializer):
    attachments = AttachmentModelSerializer(many=True, read_only=True)
    author_type = SerializerMethodField(read_only=True)


    def get_author_type(self, obj):
        return obj.author_type.model

    class Meta:
        model = Message
        fields = [
            "id",
            "attachments",
            "parent_id",
            "content",
            "chat_id",
            "author_type",
            "author_id",
            "created_date",
        ]
        read_only_fields = [
            "id",
            "attachments",
            "parent_id",
            "content",
            "author_type",
            "chat_id",
            "author_id",
            "created_date",
        ]

class MessageCreateSerializer(Serializer):
    attachment_ids = ListField(
        child=UUIDField(required=True), allow_empty=False, required=True
    )
    parent_id = UUIDField(required=False, allow_null=True)
    content = CharField(required=False)

    class Meta:
        fields = [
            "attachment_ids",
            "parent_id",
            "content",
        ]