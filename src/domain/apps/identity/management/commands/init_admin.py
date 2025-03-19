import logging
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decouple import config

User = get_user_model()
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(is_superuser=True).exists():

            logger.info("SEED | init_admin | No Admin User Seed Found!")

            User.super_users.create(
                password=config("SUPERUSER_PASSWORD"),
                email=config("SUPERUSER_EMAIL"),
            )
            logger.info("SEED | init_admin | Admin User Created.")

        else:
            logger.info("SEED | init_admin | Admin Seed Already Created")
