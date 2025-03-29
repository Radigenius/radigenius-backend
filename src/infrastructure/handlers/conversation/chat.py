from typing import Dict
from django.db import transaction

from domain.apps.conversation.models import Chat
from infrastructure.handlers.base import BaseHandler

from infrastructure.handlers.conversation.message import MessageHandler
from infrastructure.services.inference import InferenceService


class ChatHandler(BaseHandler):
    model = Chat

    def create(self, data: Dict) -> Chat:
        user_id = self.request.user.id
        title = f'Conversation ${self.model.objects.count() + 1}'
        return self.model.objects.create(user_id=user_id, title=title)


    def create_and_send_message(self, data):

        user_id = self.request.user.id
        message = data.pop("message")

        with transaction.atomic():
            message_handler = MessageHandler(self.view, self.request)        
            chat = self.model.objects.create(user_id=user_id)

            message_entity = message_handler.create({**message, "chat": chat})
            title = self.generate_conversation_title(chat, message_entity)

            chat.title = title
            chat.save(update_fields=["title"])

            return self.generate_response(chat, message_entity)


    def generate_conversation_title(self, chat, first_message = None):
        
        first_message = first_message or chat.messages.first()

        if not first_message:
            return "New Conversation"

        inference_service = InferenceService()
        return inference_service.generate_chat_title(first_message)
    
    def send_message(self, chat_id, message):

        with transaction.atomic():
            chat = self.model.objects.get_or_not_found_exception(id=chat_id)
            message_handler = MessageHandler(self.view, self.request)        
            message_entity = message_handler.create({**message, "chat": chat})

            return self.generate_response(chat, message_entity)

    
    def generate_response(self, chat, message):

        with transaction.atomic():
            message_handler = MessageHandler(self.view, self.request)        
            inference_service = InferenceService(message_handler, chat)
            return inference_service.send_message(message)

    def get_list_for_current_user(self):
        return self.model.objects.filter(user_id=self.request.user.id)

