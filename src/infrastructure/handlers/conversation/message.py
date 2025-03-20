from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from domain.apps.conversation.models import Message
from infrastructure.handlers.base import BaseHandler

User = get_user_model()

class MessageHandler(BaseHandler):
    model = Message

    def create(self, data):
        user_id = self.request.user.id
        content_type = ContentType.objects.get_for_model(User)
        
        data.pop("attachment_ids")
        data["content_type"] = content_type
        data["object_id"] = user_id
        
        return super().create(data)