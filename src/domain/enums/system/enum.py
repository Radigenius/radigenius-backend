from django.db.models import TextChoices

class AttachmentFileTypes(TextChoices):
    IMAGE = "Image"


class ModelTypes(TextChoices):
    RADIGENIUS = "RadiGenius"
