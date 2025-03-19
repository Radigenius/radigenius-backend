from django.contrib import admin

from domain.base import CustomModelAdmin, CustomModelForm, CustomStackedInline
from domain.apps.conversation.models import Message
from presentation.admin.system.attachment_admin import AttachmentInline


class MessageCreationAndChangeForm(CustomModelForm):
    class Meta:
        model = Message
        fields = ["chat", "content", "parent"]


@admin.register(Message)
class MessageAdmin(CustomModelAdmin):
    model = Message
    list_display = ("id", "chat", "content", "created_date", "updated_date")
    form = MessageCreationAndChangeForm
    inlines = [AttachmentInline]


class MessageInline(CustomStackedInline):
    model = Message
    extra = 0
    form = MessageCreationAndChangeForm