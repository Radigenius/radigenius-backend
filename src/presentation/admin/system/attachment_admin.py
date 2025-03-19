from django.contrib import admin

from domain.base import CustomModelAdmin, CustomGenericStackedInline
from domain.apps.system.models import Attachment

class AttachmentInline(CustomGenericStackedInline):
    model = Attachment
    extra = 0

@admin.register(Attachment)
class CustomAttachmentAdmin(CustomModelAdmin):
    model = Attachment
    list_display = (
        "id",
        "file_type",
        "content_type",
        "object_id",
    )