from uuid import uuid4 as GUID

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError

from domain.base import BaseModel
from domain.apps.system.models import Model
from domain.apps.conversation.managers import MessageManager

User = get_user_model()

class Message(BaseModel):
    attachments = GenericRelation("system.Attachment", on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    chat = models.ForeignKey("conversation.Chat", on_delete=models.RESTRICT, related_name="messages")
    
    # Generic relation for authorship
    author_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={'model__in': ['user', 'model']}
    )
    author_id = models.UUIDField(db_index=True, default=GUID, editable=False)
    author = GenericForeignKey('author_type', 'author_id')
    
    objects = MessageManager()

    class Meta(BaseModel.Meta):
        pass

    def clean(self):
        """Ensure author_type is User or Model for now"""
        super().clean()
        
        # Make sure author_type is User and Model model
        if self.author_type and self.author_type.model_class() not in [User, Model]:
            raise ValidationError("Currently only User and Model model are supported as author")
            
    def get_user(self):
        """Helper method to get the author as a User instance"""
        if self.author and isinstance(self.author, User):
            return self.author
        return None
