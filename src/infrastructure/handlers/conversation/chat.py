from django.db import transaction

from domain.apps.conversation.models import Chat
from infrastructure.handlers.base import BaseHandler

from domain.enums.system.enum import ModelTypes
from infrastructure.handlers.conversation.message import MessageHandler
from infrastructure.services.radigenius_model.inference import RadiGenius


class ChatHandler(BaseHandler):
    model = Chat

    def create(self, data):

        user_id = self.request.user.id
        message = data.pop("message")

        with transaction.atomic():
            message_handler = MessageHandler(self.view, self.request)        
            chat = self.model.objects.create(user_id=user_id)

            message_entity = message_handler.create({**message, "chat": chat})

            response = self.generate_response(chat, message_entity)

            title = self.generate_conversation_title(chat, message_entity)

            chat.title = title
            chat.save(update_fields=["title"])

        return chat


    def generate_conversation_title(self, chat, first_message = None):
        
        first_message = first_message or chat.messages.first()
        content = first_message.content

        if not content:
            return "New Conversation"

        model_instance = RadiGenius()
        return model_instance.generate_chat_title(content)
    
    def send_message(self, chat_id, message):

        chat = self.model.objects.get_or_not_found_exception(id=chat_id)
        message_handler = MessageHandler(self.view, self.request)        
        message_entity = message_handler.create({**message, "chat": chat})

        response_entity = self.generate_response(chat, message_entity)

        return response_entity

    
    def generate_response(self, chat, message):

        model_instance = RadiGenius()
        message_handler = MessageHandler(self.view, self.request)        
        attachments = message_handler.get_attachments(message.id)
        
        response = model_instance.send_message(message.content, attachments)

        message_handler = MessageHandler(self.view, self.request)
        response_entity = message_handler.create({"content": response, "chat": chat}, model_name=ModelTypes.RADIGENIUS)

        return response_entity

    def get_list_for_current_user(self):
        return self.model.objects.filter(user_id=self.request.user.id)

