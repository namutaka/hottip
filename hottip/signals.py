from django.db.models.signals import post_save
from django.dispatch import receiver
from apscheduler.triggers.cron import CronTrigger
from .models import Distributor
from . import schedule
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Distributor)
def distributor_handler(sender, instance, **kwargs):
    schedule.add_distoributor_emit_job(instance)

