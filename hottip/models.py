import itertools
import json
import logging
from enum import Enum

from django.db import models
from django.utils import timezone
from django.core import validators, exceptions

from . import fields, services

logger = logging.getLogger(__name__)


class Channel(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
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
        ordering = ["-created_at"]


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
        return self.title


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
    channel = models.ForeignKey(Channel,
                                on_delete=models.CASCADE,
                                related_name="distributors",
                                related_query_name="distributor")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}:{self.type}'

    def clean(self):
        self.parse_setting().clean()


    def parse_setting(self):
        if self.type == self.Type.EMAIL.name:
            return EmailSetting(self.attribute)
        elif self.type == self.Type.SLACK.name:
            return SlackSetting(self.attribute)
        elif self.type == self.Type.WEBHOOK.name:
            return WebhookSetting(self.attribute)


    def distribute(self):
        channel = self.channel
        tips = channel.take_tips(self.tips_count)

        logger.info(f'channel : {vars(channel)}')
        logger.info(f'tips : {tips}')

        if tips:
            setting = self.parse_setting()
            self.__do_distribute(tips, setting)
            DistributedLog.record_logs(tips)


    def __do_distribute(self, tips, setting):
        if self.type == self.Type.EMAIL.name:
            services.post_email(
                setting.email,
                setting.subject,
                tips
            )

        elif self.type == self.Type.SLACK.name:
            services.post_slack(
                setting.channel,
                setting.username,
                setting.icon,
                tips
            )

        elif self.type == self.Type.WEBHOOK.name:
            services.post_webhook(
                setting.webhook_url,
                tips
            )

        else:
            logger.error('Invalid distribution type: [%s]', self.type)
            raise RuntimeError(f'Invalid distribution type: [{self.type}]')


class EmailSetting:
    def __init__(self, fields):
        self.email = fields.get('email')
        self.subject = fields.get('subject')

    def clean(self):
        errors = {}

        try:
            if not self.email:
                raise exceptions.ValidationError('Missing email.', code='required')
            elif self.email:
                validators.validate_email(self.email)
        except exceptions.ValidationError as e:
            errors['email'] = e.error_list

        try:
            if not self.subject:
                raise exceptions.ValidationError('Missing subject.', code='required')
        except exceptions.ValidationError as e:
            errors['subject'] = e.error_list

        if errors:
            raise exceptions.ValidationError(errors)


class SlackSetting:
    def __init__(self, fields):
        self.channel  = fields.get('channel')
        self.username = fields.get('username')
        self.icon     = fields.get('icon')


    def clean(self):
        errors = {}

        try:
            if not self.channel:
                raise exceptions.ValidationError('Missing channel.', code='required')
        except exceptions.ValidationError as e:
            errors['channel'] = e.error_list

        try:
            if not self.username:
                raise exceptions.ValidationError('Missing username.', code='required')
        except exceptions.ValidationError as e:
            errors['username'] = e.error_list

        try:
            if not self.icon:
                raise exceptions.ValidationError('Missing icon.', code='required')
        except exceptions.ValidationError as e:
            errors['icon'] = e.error_list

        if errors:
            raise exceptions.ValidationError(errors)


class WebhookSetting:
    def __init__(self, fields):
        self.webhook_url = fields.get('webhook_url')

    def clean(self):
        errors = {}

        try:
            if not self.webhook_url:
                raise exceptions.ValidationError(_('Missing webhook_url.'), code='required')
        except exceptions.ValidationError as e:
            errors['webhook_url'] = e.error_list

        if errors:
            raise exceptions.ValidationError(errors)

