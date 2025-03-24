import logging
from PIL import Image
import torch
import os
from typing import List
from huggingface_hub import snapshot_download
from unsloth import FastVisionModel

from django.conf import settings
from django.db.models import QuerySet

from domain.apps.system.models import Attachment
from infrastructure.exceptions.exceptions import ModelInferenceException, ModelDownloadException, ModelNotInitializedException
from infrastructure.decorators.model_initialized_guard import model_initialized_guard

from .config import get_config

logger = logging.getLogger(__name__)

class RadiGenius:
    model = None
    tokenizer = None
    device = None
    is_mock = False

    def __init__(self) -> None:
        # Check if we should run in mock mode based on DEBUG setting
        RadiGenius.is_mock = getattr(settings, 'DEBUG', False)
        
        if not RadiGenius.is_mock:
            if RadiGenius.model is None or RadiGenius.tokenizer is None:
                self.initialize_model()
            
            if RadiGenius.device is None:
                self.initialize_device()
        else:
            logger.info("Running RadiGenius in mock mode (DEBUG=True)")

    @classmethod
    def initialize_model(cls):
        """Initialize and return the base model and tokenizer."""
        config = get_config()
        print('initializing model config: ', config)
        model, tokenizer = FastVisionModel.from_pretrained(**config)
        print('initializing model for inference')
        FastVisionModel.for_inference(model)

        cls.model = model
        cls.tokenizer = tokenizer

    @classmethod
    def initialize_device(cls):
        cls.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    @classmethod
    def download_model(cls):
        """
        Downloads the model files from Hugging Face Hub to the local cache directory.
        This method can be called independently to pre-download the model files.
        
        Returns:
            str: Path to the downloaded model directory
        """
        if cls.is_mock:
            logger.info("Mock mode: Skipping model download")
            return "/mock/model/path"
            
        try:
            # Get model configuration from config.py
            config = get_config()
            model_name = config["model_name"]
            cache_dir = config["cache_dir"]
            
            # Create cache directory if it doesn't exist
            os.makedirs(cache_dir, exist_ok=True)
            
            logger.info(f"Downloading model '{model_name}' to {cache_dir}...")
            
            # Download the model files
            local_dir = snapshot_download(
                repo_id=model_name,
                cache_dir=cache_dir,
                local_dir=os.path.join(cache_dir, model_name.split("/")[-1]),
                local_dir_use_symlinks=False,
                resume_download=True,
                revision="main"
            )
            
            logger.info(f"Model successfully downloaded to {local_dir}")
                
            return local_dir
        except Exception as e:
            raise ModelDownloadException(errors=str(e))

    @staticmethod
    def _create_template(content: str, attachment_count: int):

        template = [
            {"role": "user", "content": [
                *[{"type": "image"} for _ in range(attachment_count)],
                {"type": "text", "text": content}
            ]}
        ]

        return template
        
    @classmethod
    @model_initialized_guard
    def send_message(cls, content, attachments: QuerySet[Attachment]=[]):
        """
        Send a message to the model and get a response.
        If in mock mode, returns a simplified response based on the input.
        """
        if cls.is_mock:
            # Create a mock response using a portion of the input content
            mock_response = f"[MOCK RESPONSE] Echo of your prompt: '{content[:100]}...'"
            
            # Log the mock operation
            logger.info(f"Mock RadiGenius used. Input length: {len(content)}, attachments: {len(attachments)}")
            
            return mock_response
        
        try:
            template = cls._create_template(content, attachments.count())
            input_text = cls.tokenizer.apply_chat_template(template, add_generation_prompt=True)
            inputs = cls.tokenizer(input_text, add_special_tokens=False, return_tensors="pt").to(cls.device)

            images = [Image.open(attachment.file.path) for attachment in attachments.only("file")]

            output_ids = cls.model.generate(
                images,
                **inputs,
                max_new_tokens=256,
                temperature=1.5,
                min_p=0.1
            )
            generated_text = cls.tokenizer.decode(output_ids[0], skip_special_tokens=True)
            return generated_text.replace("assistant", "\n\nassistant").strip()
        except ModelNotInitializedException:
            raise
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
        cls.is_mock = False
