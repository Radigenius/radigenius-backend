import requests
from json.decoder import JSONDecodeError
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
        return f"{self.base_url}/{endpoint}/"

    @staticmethod
    def _prepare_configs(model: ModelTypes):
        return {
            "max_new_tokens": 600,
            "temperature": 0.7,
            "min_p": 0.9,
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
        stream = payload.get("configs", {}).get("stream", True)
        model = payload.get("configs", {}).get("model", ModelTypes.RADIGENIUS)
        collected = ""

        try:
            with requests.post(endpoint, json=payload, stream=stream) as response:
                if response.status_code == 200:
                    # Stream the response
                    for line in response.iter_lines():
                        if line:
                            # Decode the line as UTF-8
                            data = line.decode('utf-8')

                            # Assuming you want to handle SSE (Server-Sent Events) format:
                            if data.startswith('data: '):
                                data = data[6:]

                            collected += data
                            # Proper SSE format - each message needs data: prefix and double newlines
                            yield f"data: {data}\n\n"

                    # End of stream marker
                    yield "data: [DONE]\n\n"
                    
                    # Create the assistant message after streaming is complete
                    self._handle_message(collected, model)
                else:
                    raise Exception(response.text)

        except Exception as e:
            error_msg = str(e)
            yield f"data: [ERROR]"
            raise ModelInferenceException(errors=[{"message": error_msg}, {"code": getattr(response, 'status_code', 550)}])

    def _handle_message(self, response: str, model: ModelTypes):
        # Just create the message without returning it since we're in a streaming context
        self.message_handler.create({"content": response, "chat": self.chat}, model_name=model)

    def generate_chat_title(self, message: Message):
        return 'Model Generated Title'