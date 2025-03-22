from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from domain.base import BaseManager
from domain.apps.system.models.model import Model

User = get_user_model()

class MessageManager(BaseManager):

    def prepare_list_queryset(self, queryset=None):
        return super().prepare_list_queryset(queryset).prefetch_related("attachments")
        
    def create_for_user(self, user, **kwargs):
        """Helper method to create a message with a User author"""
        if not isinstance(user, User):
            raise ValueError("Author must be a User instance")
            
        author_type = ContentType.objects.get_for_model(User)
        return self.create(
            author_type=author_type,
            author_id=user.id,
            **kwargs
        )

    def create_for_gpt(self, model, **kwargs):
        """Helper method to create a message from llm response"""
        if not isinstance(model, Model):
            raise ValueError("Model must be a Model instance")
            
        author_type = ContentType.objects.get_for_model(Model)
        return self.create(
            author_type=author_type,
            author_id=model.id,
            **kwargs
        )
