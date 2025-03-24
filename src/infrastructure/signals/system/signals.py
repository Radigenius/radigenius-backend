import os
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save

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



@receiver(post_save, sender=Attachment)
def link_or_unlink_attachment_to_entity(sender, instance, created, **kwargs):

    if created:
        return
    
    # when the attachment is pending, we need to link it to the entity
    if 'pending' in instance.file.path and instance.object_id:
        Attachment.objects.link_to_message(instance, instance.object_id)
        logger.info(f"SIGNAL | system_signal | link_attachment_to_entity | Linked attachment to entity for file: {instance.file.path}")

    # when the attachment is not pending, we need to unlink it from the entity
    if 'pending' not in instance.file.path and not instance.object_id:
        Attachment.objects.unlink_from_message(instance.id)
        logger.info(f"SIGNAL | system_signal | unlink_attachment_from_entity | Unlinked attachment from entity for file: {instance.file.path}")