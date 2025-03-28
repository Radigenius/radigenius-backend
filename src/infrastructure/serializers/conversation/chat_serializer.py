from rest_framework.serializers import ModelSerializer, Serializer
from domain.apps.conversation.models import Chat

from infrastructure.serializers.conversation.message_serializer import MessageCreateSerializer, MessageModelSerializer

class ChatSmallModelSerializer(ModelSerializer):

    class Meta:
        model = Chat
        fields = [
            "id",
            "user_id",
            "title",
            "created_date",
        ]
        read_only_fields = [
            "id",
            "user_id",
            "title"
            "created_date",
        ]


class ChatModelSerializer(ChatSmallModelSerializer):
    messages = MessageModelSerializer(read_only=True, many=True)

    class Meta(ChatSmallModelSerializer.Meta):
        fields = ChatSmallModelSerializer.Meta.fields + [
            "messages"
        ]


class ChatCreateSerializer(Serializer):
    pass
    # message = MessageCreateSerializer(required=True)