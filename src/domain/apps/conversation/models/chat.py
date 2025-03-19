from django.db import models
from domain.base import BaseModel
from domain.apps.conversation.managers import ChatManager


class Chat(BaseModel):
    user = models.ForeignKey("identity.User", on_delete=models.RESTRICT, related_name='chats')
    title = models.CharField(max_length=255, blank=True, null=True)
    is_deleted= models.BooleanField(default=False)

    objects = ChatManager()

    class Meta(BaseModel.Meta):
        pass

    def __str__(self):
        return str(self.title)
