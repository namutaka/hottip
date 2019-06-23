import logging
import requests
import json
from django.conf import settings
from textwrap import dedent
from graphql_relay.node.node import to_global_id
from django.urls import reverse

logger = logging.getLogger(__name__)

def __channel_url(channel):
    return settings.HOTTIP_APP_BASE_URL + '/channels/' + to_global_id('ChannelNode', channel.id)

def post_email(channel, email, subject, tips):
    pass


def post_slack(channel, slack_channel, username, icon, tips):
    for tip in tips:
        text = dedent("""
                *{title}*
                {text}
            """).strip() \
            .format(title=tip.title, text=tip.text)
        logger.info(text)

        __send_slack({
            "channel": slack_channel,
            "username": username,
            "text": text,
            "icon_emoji": icon,
            "link_names": 1
        })

    __send_slack({
        "channel": slack_channel,
        "username": username,
        "text": f"送信元: {__channel_url(channel)}",
        "icon_emoji": icon,
        "link_names": 1
    })

def __send_slack(payload):
        r = requests.post(settings.SLACK_WEBHOOK_URL, data=json.dumps(payload))
        if r.status_code not in range(200, 300):
            logger.error(
                    "Failed to send slack %s, status=%s: %s",
                    settings.SLACK_WEBHOOK_URL,
                    r.status_code,
                    r.text)


def post_webhook(channel, webhook_url, tips):
    payload = {
        channel_url: __channel_url(channel),
        tips: []
    }
    for tip in tips:
        payload.tips.append({
            "title": tip.title,
            "text": tip.text,
        })

    r = requests.post(webhook_url, data=json.dumps(payload))
    if r.status_code not in range(200, 300):
        logger.error(
                "Failed to send webhook %s, status=%s: %s",
                webhook_url,
                r.status_code,
                r.text)

