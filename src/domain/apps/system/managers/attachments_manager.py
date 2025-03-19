from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image as PILImage

from domain.enums.system.enum import AttachmentFileTypes
from domain.base import BaseManager
from infrastructure.exceptions.exceptions import UnsupportedFileTypeException
import magic


class AttachmentsManager(BaseManager):
    def get_queryset(self):
        return super().get_queryset().select_related("content_type")


    def create_attachment(self, file, **kwargs):
        instance = self.model(**kwargs)
        if file:
            instance.file.save(file.name, file, save=False)
            instance.file_type = self.determine_file_type(instance.file)
            self.process_file(instance)
        return instance

    @staticmethod
    def determine_file_type(file):
        file.seek(0)
        mime_type = magic.from_buffer(file.read(1024), mime=True)

        if mime_type.startswith("image/"):
            return AttachmentFileTypes.IMAGE
        elif mime_type.startswith("video/"):
            return AttachmentFileTypes.VIDEO
        elif mime_type == "application/pdf":
            return AttachmentFileTypes.PDF
        else:
            raise UnsupportedFileTypeException(file_type=mime_type)

    def process_file(self, instance):
        processors = {
            AttachmentFileTypes.IMAGE: self._process_image,
            AttachmentFileTypes.VIDEO: self._process_video,
            AttachmentFileTypes.PDF: self._process_pdf,
        }

        processor = processors.get(instance.file_type, None)

        if not processor:
            raise UnsupportedFileTypeException(file_type=instance.file_type)

        instance = processor(instance)
        instance.file.seek(0)
        return instance

    @staticmethod
    def _process_image(instance):
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
            f"{instance.title}.webp", ContentFile(output.getvalue()), save=False
        )

        return instance

    def _process_video(self, instance):
        raise NotImplementedError("_process_video is not implemented")

    def _process_pdf(self, instance):
        raise NotImplementedError("_process_pdf is not implemented")
