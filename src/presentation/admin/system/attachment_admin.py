from django.contrib import admin

from domain.base import CustomModelAdmin, CustomGenericStackedInline, CustomModelForm
from domain.apps.system.models import Attachment

class AttachmentInline(CustomGenericStackedInline):
    model = Attachment
    extra = 0


class CustomAttachmentAddChangeForm(CustomModelForm):
    class Meta:
        model = Attachment
        fields = [
            "file",
            "content_type",
            "object_id",
        ]

@admin.register(Attachment)
class CustomAttachmentAdmin(CustomModelAdmin):
    model = Attachment
    form = CustomAttachmentAddChangeForm
    add_form = CustomAttachmentAddChangeForm
    list_display = (
        "id",
        "file_type",
        "absolute_url",
        "content_type",
        "object_id",
    )