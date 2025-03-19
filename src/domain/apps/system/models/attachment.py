from uuid import uuid4 as GUID
from decouple import config

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from domain.base import BaseModel
from domain.enums.system.enum import AttachmentFileTypes
from domain.apps.system.managers import AttachmentsManager


def upload_to(instance, filename):
    return f"{instance.content_type.model}/{instance.object_id}/{filename}"


class Attachment(BaseModel):
    file = models.FileField(upload_to=upload_to, max_length=255)
    file_type = models.CharField(max_length=10, choices=AttachmentFileTypes.choices)

    # Generic foreign key
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField(db_index=True, default=GUID, editable=False)
    content_object = GenericForeignKey("content_type", "object_id")

    objects = AttachmentsManager()

    @property
    def absolute_url(self):
        return self.url or f"{config('CDN_URL')}{self.file.url}"

    class Meta(BaseModel.Meta):
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self) -> str:
        return f"({self.file_type}) | {self.content_object} - {self.title}"

    def save(self, *args, **kwargs):
        if self.file:
            # Use create_attachment method from the manager
            new_instance = Attachment.objects.create_attachment(
                file=self.file,
                title=self.title,
                description=self.description,
                url=self.url,
                content_type=self.content_type,
                object_id=self.object_id,
            )
            # Update the current instance with the processed data
            self.file = new_instance.file
            self.file_type = new_instance.file_type

        super().save(*args, **kwargs)
