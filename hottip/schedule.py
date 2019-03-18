from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
from .models import Distributor

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()


def start():
    logger.info('Start hottip scheduler')
    scheduler.add_job(_monitor, 'interval', minutes=1)
    scheduler.start()

    for d in Distributor.objects.all():
        add_distoributor_emit_job(d)

    scheduler.print_jobs()


def add_distoributor_emit_job(distributor):
    logger.info('add distoribution job: %s', vars(distributor))
    scheduler.add_job(
        _emit_distributor,
        CronTrigger(**distributor.schedule),
        args=[distributor.id],
        id=f'distribute:{distributor.id}',
        replace_existing=True)


def _monitor():
    scheduler.print_jobs()


def _emit_distributor(distributor_id):
    distributor = Distributor.objects.get(id=distributor_id)
    logger.info(f'emitted distributor: {distributor_id}')
    distributor.distribute()


@receiver(post_save, sender=Distributor)
def distributor_handler(sender, instance, **kwargs):
    add_distoributor_emit_job(instance)

