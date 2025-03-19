import logging
from django.core.management.base import BaseCommand

from application.enums.services.enum import CacheKeys
from infrastructure.services.cache import CacheService

logger = logging.getLogger(__name__)

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        logger.info('CORE | invalidate_caches | Invalidating Caches...')

        for cache_key in CacheKeys:
            CacheService.delete(cache_key.key)
            logger.info(f'CORE | invalidate_caches | Invalidated {cache_key.key} Cache')
        
        logger.info('CORE | invalidate_caches | Invalidated All Caches!')