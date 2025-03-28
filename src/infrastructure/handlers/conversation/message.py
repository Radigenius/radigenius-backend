from django.db import transaction
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models import QuerySet
from domain.apps.conversation.models import Message
from domain.apps.system.models import Attachment, Model
from infrastructure.handlers.base import BaseHandler
from infrastructure.exceptions.exceptions import ValidationException

User = get_user_model()

class MessageHandler(BaseHandler):
    model = Message

    def create(self, data, model_name=None):

        with transaction.atomic():

            attachment_ids = data.pop("attachment_ids", [])
            attachments = Attachment.objects.filter(id__in=attachment_ids)

            # Attachments are required for user messages
            if not model_name and not attachments.exists():
                raise ValidationException("Attachments are required")
            
            if model_name:
                model = Model.objects.get_or_not_found_exception(name=model_name)
                message = Message.objects.create_for_gpt(model, **data)
            else:
                user = self.request.user
                message = Message.objects.create_for_user(user, **data)
            
            # Link attachments to the message
            Attachment.objects.batch_link_attachment_to_message(attachments, message.id)
        
        return message

    def get_attachments(self, message_id) -> QuerySet[Attachment]:
        content_type = ContentType.objects.get_for_model(Message)
        return Attachment.objects.filter(object_id=message_id, content_type=content_type)