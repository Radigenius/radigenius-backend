from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from domain.apps.conversation.models import Message
from infrastructure.handlers.base import BaseHandler
from domain.apps.system.models import Attachment

User = get_user_model()

class MessageHandler(BaseHandler):
    model = Message

    def create(self, data):
        user = self.request.user
        attachment_ids = data.pop("attachment_ids", [])
        
        message = Message.objects.create_for_user(user, **data)
        
        # Link attachments to the message if any provided
        if attachment_ids:
            Attachment.objects.link_attachments_to_message(attachment_ids, message.id)
        
        return message