import requests

from domain.apps.conversation.models import Message, Chat
from domain.enums.system.enum import ModelTypes

from infrastructure.exceptions.exceptions import ModelInferenceException

from decouple import config

class InferenceService:

    message_handler = None
    chat: Chat

    def __init__(self, message_handler, chat: Chat):
        self.base_url = config("INFERENCE_SERVICE_URL")
        self.message_handler = message_handler
        self.chat = chat

    def _prepare_endpoint(self, endpoint: str):
        return f"{self.base_url}/{endpoint}"

    @staticmethod
    def _prepare_configs(model: ModelTypes):
        return {
            "max_new_tokens": 500,
            "temperature": 0.7,
            "min_p": 0.05,
            "model": model,
            "stream": True,
        }

    def _prepare_payload(self, message: Message):
        return {
            "configs": self._prepare_configs(ModelTypes.RADIGENIUS),
            "conversation_history": self._get_conversation_history(),
            "message": self._prepare_message(message),
        }

    def _prepare_message(self, message: Message):
        
        attachments = self.message_handler.get_attachments(message.id)
        
        return {
            "role": "user" if message.author_type.name == "user" else "assistant",
            "content": [
                {
                    "type": "text",
                    "text": message.content,
                },
                *[
                    {
                        "type": "image",
                        "image": attachment.absolute_url,
                    }
                    for attachment in attachments
                ]
            ]
        }

    def _get_conversation_history(self):
        
        messages = self.chat.messages.order_by("created_date")
        return [self._prepare_message(message) for message in messages]


    def is_service_healthy(self):
        endpoint = self._prepare_endpoint("inference/healthy")
        response = requests.get(endpoint)
        return response.json()


    def send_message(self, message: Message):

      endpoint = self._prepare_endpoint("inference")
      payload = self._prepare_payload(message)

      collected = ""

      with requests.post(endpoint, json=payload, stream=True) as response:
        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    data = line.decode('utf-8')
                    if data.startswith('data: '):
                        data = data[6:]

                    collected += data
                    yield data
        else:
            raise ModelInferenceException(f"response: {response.text}")

      return self._handle_message(collected, payload)

    def _handle_message(self, response: str, payload):
        return self.message_handler.create({"content": response, "chat": self.chat}, model_name=payload.get("model"))

    def generate_chat_title(self, message: Message):
        return 'Model Generated Title'