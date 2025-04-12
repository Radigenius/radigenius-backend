from django.db.models import Q

from rest_framework.response import Response
from rest_framework import status
from django.http import StreamingHttpResponse

from infrastructure.commands.base import BaseCommand
from infrastructure.handlers.conversation import ChatHandler


class ChatCommand(BaseCommand):
    handler = ChatHandler

    # def create(self, data):

    #     validated_data = self.validate(data)
    #     handler = self.handler(self.view, self.request)
    #     chat = handler.create(validated_data)

    #     return StreamingHttpResponse(
    #         streaming_content=handler.send_message(chat.id, validated_data),
    #         content_type='text/event-stream'
    #     )
    

    def send_message(self, chat_id, message):
        validated_data = self.validate(message)
        
        handler = self.handler(self.view, self.request)
        response = StreamingHttpResponse(
            streaming_content=handler.send_message(chat_id, validated_data),
            content_type='text/event-stream'
        )
        
        # These headers are crucial for SSE to work properly
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'  # Important if you later use Nginx
        
        return response
