from django.contrib import admin

from domain.base import CustomModelAdmin, CustomModelForm
from domain.apps.conversation.models import Chat
from presentation.admin.conversation.message_admin import MessageInline

class ChatCreationAndChangeForm(CustomModelForm):
    class Meta:
        model = Chat
        fields = ["title", "user"]

@admin.register(Chat)
class ChatAdmin(CustomModelAdmin):
    model = Chat
    list_display = ("id", "title", "user", "created_date", "updated_date")
    form = ChatCreationAndChangeForm
    inlines = [MessageInline]