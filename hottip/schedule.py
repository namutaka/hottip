from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import logging
from .models import Distributor
from apscheduler.triggers.cron import CronTrigger

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()

def start():
    logger.info('Start hottip scheduler')
    scheduler.add_job(run, 'interval', minutes=1)
    scheduler.start()

    for d in Distributor.objects.all():
        add_distoributor_emit_job(d)

    scheduler.print_jobs()

def run():
    logger.info('do')
    print('do')
    scheduler.print_jobs()

def add_distoributor_emit_job(distributor):
    logger.info('add distoribution job:', vars(distributor))
    scheduler.add_job(
            emitted,
            CronTrigger.from_crontab(distributor.schedule),
            args=[distributor.id],
            id=f'distribute:{distributor.id}')

def emitted(distributor_id):
    distributor = Distributor.objects.get(id=distributor_id)
    logger.info(f'emitted {distributor_id}: {vars(distributor)}')

