import os
from django.dispatch import receiver
from django.db.models.signals import post_delete

from domain.apps.system.models import (
    Attachment,
)
import logging

logger = logging.getLogger(__name__)

@receiver(post_delete, sender=Attachment)
def delete_uploaded_attachment_on_entity_deletion(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
            logger.info(f"SIGNAL | system_signal | delete_uploaded_attachment_on_entity_deletion | Deleted uploaded attachment on entity deletion for file: {instance.file.path}")