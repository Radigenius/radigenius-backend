from uuid import uuid4 as GUID
from decouple import config

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from domain.base import BaseModel
from domain.enums.system.enum import AttachmentFileTypes
from domain.apps.system.managers import AttachmentsManager


def upload_to(instance, filename):
    # Handle case where object_id might be None initially
    object_folder = instance.object_id if instance.object_id else "pending"
    return f"{instance.content_type.model}/{object_folder}/{filename}"


class Attachment(BaseModel):
    file = models.FileField(upload_to=upload_to, max_length=255)
    file_type = models.CharField(max_length=10, choices=AttachmentFileTypes.choices)

    # Generic foreign key
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField(db_index=True, null=True, blank=True)
    content_object = GenericForeignKey("content_type", "object_id")

    objects = AttachmentsManager()

    @property
    def absolute_url(self):
        return f"{config('CDN_URL')}{self.file.url}"

    class Meta(BaseModel.Meta):
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self) -> str:
        return f"({self.file_type}) | {self.content_object}"

    def save(self, *args, **kwargs):
        if self.file and not self.id:
            # Use create_attachment method from the manager only for new file uploads
            new_instance = Attachment.objects.create_attachment(
                file=self.file,
                content_type=self.content_type,
                object_id=self.object_id,
            )
            # Update the current instance with the processed data
            self.file = new_instance.file
            self.file_type = new_instance.file_type

        super().save(*args, **kwargs)
