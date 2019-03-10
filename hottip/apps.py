from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class HottipConfig(AppConfig):
    name = 'hottip'

    def ready(self):
        logger.info('hottip ready')
        from hottip import schedule
        # schedule.start()

