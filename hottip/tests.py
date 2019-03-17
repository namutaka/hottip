import datetime
from pprint import pprint
from textwrap import dedent

from django.test import TestCase

from .models import Channel, DistributedLog, Distributor, Tip


class ChannelModelTests(TestCase):

    def test_take_tips(self):
        channel = Channel.objects.create(name='text')
        for n in range(1, 5):
            tip = Tip.objects.create(title=f'tip{n}')
            channel.assignment_set.create(tip=tip)

        print("test_take_tips")
        act = channel.take_tips(2)
        pprint(act)


    def test_take_tips__with_logs(self):
        channel = Channel.objects.create(name='text')
        for n in range(1, 6):
            tip = Tip.objects.create(title=f'tip{n}')
            channel.assignment_set.create(tip=tip)

        assigns = channel.assignment_set.all()[1:4]
        DistributedLog.record_logs(assigns)

        print("test_take_tips__with_logs")
        act = channel.take_tips(3)
        pprint(act)


class DistributorModelTests(TestCase):

    def test_distribute(self):
        channel = Channel.objects.create(name='text')
        for n in range(1, 3):
            tip = Tip.objects.create(
                    title=f'tip{n}',
                    text=dedent("""
                        test message

                        https://text.example.com/hoge
                        #random
                        @here
                        text end
                    """).strip()
                    )
            channel.assignment_set.create(tip=tip)

        distributor = Distributor(
            type=Distributor.Type.SLACK,
            channel=channel,
            tips_count=2,
            attribute="""
            {
            "channel": "#general",
            "icon": ":ghost:",
            "username": "HotTipです"
            }
            """)
        distributor.distribute()

        act_log = list(DistributedLog.objects.all())

        print("xxx")
        pprint(act_log)

    def attribute_field(self):
        channel = Channel.objects.create(name='text')
        distributor = Distributor(
            channel=channel,
            type=Distributor.Type.SLACK,
            tips_count=2,
            attribute= {
                "channel": "#general",
                "icon": ":ghost:",
                "username": "HotTipです"
            },
            schedule="1 1 * * *")

        print(distributor.attribute)

        distributor.save()

        act = Distributor.objects.all()[0]
        print(act.attribute)



class DistributedLogModelTests(TestCase):

    def test_recent_logs_by_channel(self):
        channel = Channel.objects.create(name='text')
        for n in range(1, 5):
            tip = Tip.objects.create(title=f'tip{n}')
            channel.assignment_set.create(tip=tip)

        assigns = channel.assignment_set.all()[:3]
        DistributedLog.record_logs(assigns)

        logs = list(DistributedLog.recent_logs_by_channel(channel.id, 2))
        pprint(logs)

    def test_recent_logs_by_channel__channel_not_exists(self):
        logs = list(DistributedLog.recent_logs_by_channel(99, 2))
        pprint(logs)

