from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
import logging
from .models import Distributor

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()

def start():
    scheduler.configure(timezone=settings.TIME_ZONE)

    scheduler.add_job(_reload_jobs, 'interval', minutes=1, id='reload_jobs')
    _reload_jobs()

    logger.info('Start hottip scheduler')
    scheduler.start()


def setup_distributor_jobs():
    for distributor in Distributor.objects.all():
        logger.info('add distoribution job: %s', distributor)
        scheduler.add_job(
            _emit_distributor,
            CronTrigger(**distributor.schedule),
            args=[distributor.id],
            id=f'distribute:{distributor.id}',
            replace_existing=True)


def _reload_jobs():
    setup_distributor_jobs()
    scheduler.print_jobs()


def _emit_distributor(distributor_id):
    distributor = Distributor.objects.get(id=distributor_id)
    logger.info(f'emitted distributor: {distributor_id}')
    distributor.distribute()

