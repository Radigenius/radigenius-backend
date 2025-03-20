from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    CharField,
    UUIDField,
    ListField,
)
from domain.apps.conversation.models import Message
from infrastructure.validators.identity.serializer_validators import (
    EitherFieldRequired,
)

class MessageModelSerializer(ModelSerializer):

    class Meta:
        model = Message
        fields = [
            "id",
            "attachments",
            "parent_id",
            "content",
            "chat_id",
            # "author_id",
            "created_date",
        ]
        read_only_fields = [
            "id",
            "attachments",
            "parent_id",
            "content",
            "chat_id",
            # "author_id",
            "created_date",
        ]

class MessageCreateSerializer(Serializer):
    attachment_ids = ListField(
        child=UUIDField(required=False), allow_empty=True, required=False
    )
    parent_id = UUIDField(required=False, allow_null=True)
    content = CharField(required=False)

    class Meta:
        fields = [
            "attachment_ids",
            "parent_id",
            "content",
        ]
        validators = [
            EitherFieldRequired(field_name="attachment_ids", field2="content"),
        ]


# class NewMessageSerializer(MessageMixinSerializer):
    
#     class Meta(MessageMixinSerializer.Meta):
#         pass


# class AddMessageSerializer(MessageMixinSerializer):
#     chat_id = UUIDField(required=True)
    
#     class Meta(MessageMixinSerializer.Meta):
#         fields = MessageMixinSerializer.Meta.fields + [
#             "chat_id",
#         ]


