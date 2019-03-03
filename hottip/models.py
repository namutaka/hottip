from django.db import models
from django.utils import timezone
from enum import Enum


class Tip(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    enable = models.BooleanField(default=True)
    created_at = models.DateTimeField(
            default=timezone.now)
    updated_at = models.DateTimeField(
            default=timezone.now)

    def __str__(self):
        return self.title

class Channel(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(
            default=timezone.now)
    updated_at = models.DateTimeField(
            default=timezone.now)

    tips = models.ManyToManyField(Tip, through='Assignment')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('name', ), )

class Assignment(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    tip = models.ForeignKey(Tip, on_delete=models.CASCADE)
    power = models.IntegerField(default=100)

    class Meta:
        unique_together = (('tip', 'channel', ), )

class NotifiedHistory(models.Model):
    assignment = models.ForeignKey('hottip.Assignment', on_delete=models.CASCADE)
    notified_at = models.DateTimeField(default=timezone.now)

class Distributor(models.Model):
    class Type(Enum):
        EMAIL = 'Email'
        SLACK = 'Slack'
        WEBHOOK = 'Webhook'

        @classmethod
        def choices(cls):
            return [(m.name, m.value) for m in cls]

    schedule = models.CharField(max_length=200)
    type = models.CharField(max_length=200,
        choices=Type.choices())
    attibute = models.TextField()
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)



