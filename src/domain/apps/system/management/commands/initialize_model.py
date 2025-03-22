import logging
from django.core.management.base import BaseCommand

from infrastructure.services.radigenius_model.inference import RadiGenius

logger = logging.getLogger(__name__)

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        logger.info('CORE | initialize_model | Initializing Model...')

        RadiGenius.initialize_model()

        logger.info('CORE | initialize_model | Model Initialized!')