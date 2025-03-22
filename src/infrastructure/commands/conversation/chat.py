from django.db.models import Q

from rest_framework.response import Response
from rest_framework import status

from infrastructure.commands.base import BaseCommand
from infrastructure.handlers.conversation import ChatHandler


class ChatCommand(BaseCommand):
    handler = ChatHandler

    # def create(self, data):

    #     validated_data = self.validate(data)
    #     handler = self.handler(self.view, self.request)
    #     chat = handler.create(validated_data)
    #     serializer = self.view.get_output_serializer(chat)

    #     return Response(data={"data": serializer.data}, status=status.HTTP_201_CREATED)
    

    def send_message(self, chat_id, message):
        validated_data = self.validate(message)
        
        handler = self.handler(self.view, self.request)
        entity = handler.send_message(chat_id, validated_data)
        serializer = self.view.get_output_serializer(entity)

        return Response(data={"data": serializer.data}, status=status.HTTP_201_CREATED)
