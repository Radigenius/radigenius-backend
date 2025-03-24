from io import BytesIO
from PIL import Image as PILImage
from pathlib import Path
import magic
import logging

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import QuerySet


from domain.base import BaseManager
from domain.enums.system.enum import AttachmentFileTypes
from domain.apps.system.models.attachment import Attachment
from infrastructure.exceptions.exceptions import UnsupportedFileTypeException


class AttachmentsManager(BaseManager):
    def get_queryset(self):
        return super().get_queryset().select_related("content_type")


    def create_attachment(self, file, **kwargs):
        instance = self.model(**kwargs)
        file_name = file.name.split(".")[0]
        if file:
            instance.file.save(file.name, file, save=False)
            instance.file_type = self.determine_file_type(instance.file)
            self.process_file(instance, file_name)
        return instance

    @staticmethod
    def determine_file_type(file):
        file.seek(0)
        mime_type = magic.from_buffer(file.read(1024), mime=True)

        if mime_type.startswith("image/"):
            return AttachmentFileTypes.IMAGE
        # elif mime_type.startswith("video/"):
        #     return AttachmentFileTypes.VIDEO
        # elif mime_type == "application/pdf":
        #     return AttachmentFileTypes.PDF
        else:
            raise UnsupportedFileTypeException(file_type=mime_type)

    def process_file(self, instance, file_name):
        processors = {
            AttachmentFileTypes.IMAGE: self._process_image,
            # AttachmentFileTypes.VIDEO: self._process_video,
            # AttachmentFileTypes.PDF: self._process_pdf,
        }

        processor = processors.get(instance.file_type, None)

        if not processor:
            raise UnsupportedFileTypeException(file_type=instance.file_type)

        instance = processor(instance, file_name)
        instance.file.seek(0)
        return instance

    @staticmethod
    def _process_image(instance, file_name):
        # Open the original image
        img = PILImage.open(instance.file)

        # Set the maximum size for the thumbnail
        max_size = (800, 800)
        img.thumbnail(max_size, PILImage.LANCZOS)

        # Create a BytesIO object to hold the processed image
        output = BytesIO()

        # Save the image in WebP format with reduced quality
        img.save(output, format="WebP", quality=85)
        output.seek(0)

        # Overwrite the original file with the new image (no new filename)
        instance.file.delete(
            save=False
        )  # Delete the original file before saving the new one
        instance.file.save(
            f"{file_name}.webp", ContentFile(output.getvalue()), save=False
        )

        return instance

    def _process_video(self, instance):
        raise NotImplementedError("_process_video is not implemented")

    def _process_pdf(self, instance):
        raise NotImplementedError("_process_pdf is not implemented")
        
    def link_to_message(self, attachment: Attachment, message_id):
        """
        Links an attachment to a message by setting its object_id
        and updating file storage path if necessary.
        
        Args:
            attachment: Attachment instance to update
            message_id: UUID of the message to link to
            
        Returns:
            Attachment: The updated attachment instance
            
        Raises:
            self.model.DoesNotExist: If attachment with given ID doesn't exist
            IOError: If file operations fail
        """
        # Store the current file path before updating object_id
        old_path = attachment.file.path
        is_pending = "pending" in old_path
        save_fields = []
        
        # Update object_id and save to get new path
        if not attachment.object_id:
            attachment.object_id = message_id
            save_fields.append('object_id')
        
        # Only move the file if it was previously in a pending state
        if old_path and is_pending and default_storage.exists(old_path):
            try:
                
                # Generate the new path based on upload_to function
                filename = Path(attachment.file.name).name
                
                # Create a new file at the correct location and copy content
                with default_storage.open(old_path, 'rb') as source:
                    attachment.file.save(filename, source, save=False)
                    save_fields.append('file')
                
                # Delete the old file
                default_storage.delete(old_path)
                
            except Exception as e:
                logging.error(f"Error linking attachment to message: {e}")

        attachment.save(update_fields=save_fields)
        
        return attachment

    def unlink_from_message(self, attachment: Attachment):

        update_fields = []
        filename = Path(attachment.file.name).name
        old_path = attachment.file.path

        if attachment.object_id:
            attachment.object_id = None
            update_fields.append('object_id')

        # move the file to the pending folder
        if attachment.file and old_path and default_storage.exists(old_path):

            try:
                # Create a new file at the correct location and copy content
                with default_storage.open(old_path, 'rb') as source:
                    attachment.file.save(filename, source, save=False)
                update_fields.append('file')
                
                # Delete the old file
                default_storage.delete(old_path)

            except Exception as e:
                logging.error(f"Error unlinking attachment from message: {e}")

        attachment.save(update_fields=update_fields)

        return attachment
        
    def batch_link_attachment_to_message(self, attachments: QuerySet[Attachment], message_id):
        """
        Links multiple attachments to a message by setting their object_id.
        
        Args:
            attachments (QuerySet[Attachment]): Queryset of attachments to link
            message_id (UUID): The ID of the message to link attachments to
            
        Returns:
            int: Number of attachments linked
        """
        count = 0
        
        # Link each attachment to the message
        for attachment in attachments:
            try:
                self.link_to_message(attachment, message_id)
                count += 1
            except Exception as e:
                logging.error(f"Failed to link attachment {attachment.id} to message {message_id}: {e}")
            
        return count