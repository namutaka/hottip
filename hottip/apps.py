import sys
import logging
from django.apps import AppConfig
from django.conf import settings

logger = logging.getLogger(__name__)

class HottipConfig(AppConfig):
    name = 'hottip'

    def ready(self):
        if len(sys.argv) >= 2 and sys.argv[1] != 'runserver':
            return

        logger.info('hottip ready')

        if settings.HOTTIP_BATCH_MODE:
            from hottip import schedule
            schedule.start()
