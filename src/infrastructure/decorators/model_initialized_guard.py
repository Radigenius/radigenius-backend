import logging
from typing import Callable
from functools import wraps

from infrastructure.exceptions.exceptions import ModelNotInitializedException

logger = logging.getLogger(__name__)

def model_initialized_guard(func: Callable):
    """
    Decorator that checks if the RadiGenius model and tokenizer are initialized
    before executing the decorated method. If either is None, it raises 
    ModelNotInitializedException.
    
    If RadiGenius.is_mock is True, the check is skipped, allowing for development
    mode without model initialization.
    """
    @wraps(func)
    def wrapper(cls, *args, **kwargs):
        # Skip the check if in mock mode
        if hasattr(cls, 'is_mock') and cls.is_mock:
            return func(cls, *args, **kwargs)
            
        if cls.model is None or cls.tokenizer is None:
            logger.error("Attempted to use RadiGenius model before initialization")
            raise ModelNotInitializedException(
                message="RadiGenius model is not initialized. Please ensure the model is downloaded and initialized before use.",
                errors=[f"Model or tokenizer is None"]
            )
        return func(cls, *args, **kwargs)
    return wrapper