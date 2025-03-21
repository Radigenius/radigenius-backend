from unsloth import FastVisionModel

from .config import get_config


def initialize_model():
    """Initialize and return the base model and tokenizer."""
    config = get_config()
    model, tokenizer = FastVisionModel.from_pretrained(**config)
    FastVisionModel.for_inference(model)
    return model, tokenizer