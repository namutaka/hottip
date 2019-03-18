import itertools
import json
import logging
from enum import Enum

from django.db import models
from django.utils import timezone

from . import fields, services

logger = logging.getLogger(__name__)


class Channel(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'id:{self.id},name:{self.name}'

    def take_tips(self, count):
        """通知するtipsを指定件数取得する

        過去の履歴の中でまだ使っていないTipsを取得する
        """

        tips = self.tips.filter(enable=True)

        # 取得対象tips数分の過去を取得して利用済みidを取得
        logs = DistributedLog.recent_logs_by_channel(self.id, len(tips))
        recent_tip_ids = set( log.tip.id for log in logs )

        # 利用済みではない範囲でtipsを取得
        candidates = list(tips.exclude(pk__in=recent_tip_ids).order_by('id')[:count])

        # 必要数に足りなければ、不足分を取得
        candidate_size = len(candidates)
        if candidate_size < count:
            adds_size = count - candidate_size
            adds = list(tips.exclude(pk__in=[a.id for a in candidates])
                    .order_by('id')[:adds_size])
            candidates = candidates + adds

        return candidates


    class Meta:
        unique_together = (('name', ), )


class Tip(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    enable = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    channel = models.ForeignKey(Channel,
                                on_delete=models.CASCADE,
                                related_name="tips",
                                related_query_name="tip")

    def __str__(self):
        return f'{self.id}'


class DistributedLog(models.Model):
    tip = models.ForeignKey(Tip, on_delete=models.CASCADE)
    distributed_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.id}:{self.tip}'

    @staticmethod
    def recent_logs_by_channel(channel_id, count):
        logs = DistributedLog.objects \
            .filter(tip__channel=channel_id) \
            .order_by('-distributed_at')

        return logs[:count]

    @staticmethod
    def record_logs(tips):
        DistributedLog.objects.bulk_create([
            DistributedLog(tip=t) for t in tips
        ])


class Distributor(models.Model):
    class Type(Enum):
        EMAIL = 'Email'
        SLACK = 'Slack'
        WEBHOOK = 'Webhook'

        @classmethod
        def choices(cls):
            return [(m.name, m.value) for m in cls]

    schedule = fields.JsonField(default={
        'month': '*', 'day': 1, 'day_of_week': '*', 'hour': '*', 'minute': '*'
    })
    type = models.CharField(max_length=200, choices=Type.choices())
    attribute = fields.JsonField(default={})
    tips_count = models.IntegerField(default=1)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}:{self.type}'


    def distribute(self):
        channel = self.channel
        tips = channel.take_tips(self.tips_count)

        logger.info(f'channel : {vars(channel)}')
        logger.info(f'tips : {tips}')

        if tips:
            self.__do_distribute(tips)
            DistributedLog.record_logs(tips)


    def __do_distribute(self, tips):
        if self.type == self.Type.EMAIL.name:
            services.post_email(
                self.attribute['email'],
                self.attribute['subject'],
                tips
            )

        elif self.type == self.Type.SLACK.name:
            services.post_slack(
                self.attribute['channel'],
                self.attribute['username'],
                self.attribute['icon'],
                tips
            )

        elif self.type == self.Type.WEBHOOK.name:
            services.post_webhook(
                self.attribute['webhook_url'],
                tips
            )

        else:
            logger.error('Invalid distribution type: [%s]', self.type)
            raise RuntimeError(f'Invalid distribution type: [{self.type}]')

