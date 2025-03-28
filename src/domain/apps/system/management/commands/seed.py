import logging
from django.core.management.base import BaseCommand

from domain.apps.identity.management.commands.init_admin import (
    Command as SuperUserCommand,
)
from domain.apps.system.management.commands.model_seed import Command as ModelSeedCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        logger.info("SEED | seed | Seed Started...")

        SuperUserCommand().handle(*args, **options)
        ModelSeedCommand().handle(*args, **options)

        logger.info("SEED | seed | Seed Finished!")
