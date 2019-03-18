import datetime
from pprint import pprint
from textwrap import dedent

from django.test import TestCase

from .models import Channel, DistributedLog, Distributor, Tip


class ChannelModelTests(TestCase):

    def test_take_tips(self):
        channel = Channel.objects.create(name='text')
        for n in range(1, 5):
            tip = Tip.objects.create(channel=channel, title=f'tip{n}')

        print("test_take_tips")
        act = channel.take_tips(2)
        pprint(act)


    def test_take_tips__with_logs(self):
        channel = Channel.objects.create(name='text')
        for n in range(1, 6):
            tip = Tip.objects.create(channel=channel, title=f'tip{n}')

        tips = channel.tips.all()[1:4]
        DistributedLog.record_logs(tips)

        print("test_take_tips__with_logs")
        act = channel.take_tips(3)
        pprint(act)


class DistributorModelTests(TestCase):
    def __create_tips(self, channel, size):
        for n in range(1, size):
            Tip.objects.create(
                channel=channel,
                title=f'tip{n}',
                text=dedent("""
                    test message

                    https://text.example.com/hoge
                    #random
                    @here
                    text end
                """).strip()
                )

    def test_distribute(self):
        channel = Channel.objects.create(name='text')
        self.__create_tips(channel, 3)

        distributor = Distributor(
            type=Distributor.Type.SLACK.name,
            channel=channel,
            tips_count=2,
            attribute= {
                "channel": "#general",
                "icon": ":ghost:",
                "username": "HotTipです"
            })
        distributor.distribute()

        act_log = list(DistributedLog.objects.all())

        pprint(act_log)

    def test_attribute_field(self):
        channel = Channel.objects.create(name='text')
        self.__create_tips(channel, 3)

        distributor = Distributor(
            channel=channel,
            type=Distributor.Type.SLACK.name,
            tips_count=2,
            attribute= {
                "channel": "#general",
                "icon": ":ghost:",
                "username": "HotTipです"
            },
            schedule={})

        print(distributor.attribute)

        distributor.save()

        act = Distributor.objects.all()[0]
        print(act.attribute)
        print(act.type)

        act.distribute()


class DistributedLogModelTests(TestCase):

    def test_recent_logs_by_channel(self):
        channel = Channel.objects.create(name='text')
        for n in range(1, 5):
            tip = Tip.objects.create(channel=channel, title=f'tip{n}')

        tips = channel.tips.all()[:3]
        DistributedLog.record_logs(tips)

        logs = list(DistributedLog.recent_logs_by_channel(channel.id, 2))
        pprint(logs)

    def test_recent_logs_by_channel__channel_not_exists(self):
        logs = list(DistributedLog.recent_logs_by_channel(99, 2))
        pprint(logs)

