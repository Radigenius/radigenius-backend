from domain.apps.conversation.models import Chat
from infrastructure.handlers.base import BaseHandler

from infrastructure.handlers.conversation.message import MessageHandler

class ChatHandler(BaseHandler):
    model = Chat

    def create(self, data):

        user_id = self.request.user.id
        message = data.pop("message")
        
        message_handler = MessageHandler(self.view, self.request)        
        chat = self.model.objects.create(user_id=user_id)

        message_entity = message_handler.create({**message, "chat": chat})
        title = self.generate_conversation_title(chat, message_entity)

        chat.title = title
        chat.save(update_fields=["title"])

        return chat


    def generate_conversation_title(self, chat, first_message = None):
        
        first_message = first_message or chat.messages.first()
        content = first_message.content
        
        if not content:
            return "New Conversation"
        
        return "Model Generated Title"
    
    def send_message(self, chat_id, message):

        chat = self.model.objects.get_or_not_found_exception(id=chat_id)
        message_handler = MessageHandler(self.view, self.request)        
        message_entity = message_handler.create({**message, "chat": chat})

        return message_entity

    def get_list_for_current_user(self):
        return self.model.objects.filter(user_id=self.request.user.id)

