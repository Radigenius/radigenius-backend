import logging
from django.core.management.base import BaseCommand
from decouple import config

from domain.apps.system.models import Model
from domain.enums.system.enum import ModelTypes
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not Model.objects.all().exists():

            logger.info("SEED | model_seed | No Model Seed Found!")

            Model.objects.create(
                name=ModelTypes.RADIGENIUS,
                description="RadiGenius Model",
            )
            logger.info("SEED | model_seed | Model Created.")

        else:
            logger.info("SEED | model_seed | Model Seed Already Created")
