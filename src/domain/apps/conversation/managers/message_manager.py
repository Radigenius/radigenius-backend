from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from domain.base import BaseManager

User = get_user_model()

class MessageManager(BaseManager):
        
    def create_for_user(self, user, **kwargs):
        """Helper method to create a message with a User author"""
        if not isinstance(user, User):
            raise ValueError("Author must be a User instance")
            
        content_type = ContentType.objects.get_for_model(User)
        return self.create(
            content_type=content_type,
            object_id=user.id,
            **kwargs
        )
