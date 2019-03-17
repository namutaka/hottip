import logging
import requests
import json
from django.conf import settings
from textwrap import dedent

logger = logging.getLogger(__name__)


def post_mail():
    pass


def post_slack(channel, username, icon, tips):

    for tip in tips:
        text = dedent("""
                *{title}*
                {text}
            """).strip() \
            .format(title=tip.title, text=tip.text)
        logger.info(text)

        payload = {
            "channel": channel,
            "username": username,
            "text": text,
            "icon_emoji": icon,
            "link_names": 1
        }

        r = requests.post(settings.SLACK_WEBHOOK_URL, data=json.dumps(payload))
        if r.status_code not in range(200, 300):
            logger.error(
                    "Failed to send slack {}, status={}",
                    webhook_url,
                    r.status_code)


def post_webhook(webhook_url, tips):
    for tip in tips:
        payload = {
            "title": tip.title,
            "text": tip.text,
        }

        r = requests.post(webhook_url, data=json.dumps(payload))
        if r.status_code not in range(200, 300):
            logger.error(
                    "Failed to send webhook {}, status={}",
                    webhook_url,
                    r.status_code)

