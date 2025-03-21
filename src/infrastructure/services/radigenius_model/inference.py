from PIL import Image
import torch
from typing import List

from domain.apps.system.models import Attachment
from .model_utils import initialize_model
from infrastructure.exceptions.exceptions import ModelInferenceException

class RadiGenius:
    model = None
    tokenizer = None
    device = None

    def __init__(self) -> None:
        
        if RadiGenius.model is None or RadiGenius.tokenizer is None:
            self.initialize_model()
        
        if RadiGenius.device is None:
            self.initialize_device()

    @classmethod
    def initialize_model(cls):
        model, tokenizer = initialize_model()
        cls.model = model
        cls.tokenizer = tokenizer

    @classmethod
    def initialize_device(cls):
        cls.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    @staticmethod
    def _create_template(content: str, attachments: List[Attachment]=[]):

        template = [{"role": "user", "content": [
            {"type": "text", "text": content}
        ]}]
        
        for attachment in attachments:
            image = Image.open(attachment.file.path)
            template.append({"type": "image", "image": image})

        return template
        
    @classmethod
    def send_message(cls, content, attachments=[]):
        try:
            template = cls._create_template(content, attachments)
            input_text = cls.tokenizer.apply_chat_template(template, add_generation_prompt=True)
            inputs = cls.tokenizer(input_text, add_special_tokens=False, return_tensors="pt").to(cls.device)
            
            output_ids = cls.model.generate(
                **inputs,
                max_new_tokens=256,
                temperature=1.5,
                min_p=0.1
            )
            generated_text = cls.tokenizer.decode(output_ids[0], skip_special_tokens=True)
            return generated_text.replace("assistant", "\n\nassistant").strip()
        except Exception as e:
            raise ModelInferenceException(errors=e)

    @classmethod
    def generate_chat_title(cls, content):
        return cls.send_message(content=content)

    @classmethod
    def kill_model(cls):
        cls.model = None
        cls.tokenizer = None
        cls.device = None
