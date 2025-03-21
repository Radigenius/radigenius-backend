import logging
from django.core.management.base import BaseCommand

from domain.apps.system.management.commands.seed import Command as SeedCommand
from domain.apps.system.management.commands.invalidate_caches import Command as InvalidateCacheCommand
from domain.apps.system.management.commands.initialize_model import Command as InitializeModelCommand

logger = logging.getLogger(__name__)

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        logger.info('CORE | init | Initializing...')
        
        SeedCommand().handle(*args, **options)
        InitializeModelCommand().handle(*args, **options)
        # InvalidateCacheCommand().handle(*args, **options)

        logger.info('CORE | init | Initialized Core!')