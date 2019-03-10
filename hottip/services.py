import logging
import requests
import json

logger = logging.getLogger(__name__)


def post_mail():
    pass


def post_slack(webhook_url, channel, message):
    payload = {
        "channel": channel,
        "username": "hottip",
        "text": message,
        "icon_emoji": ":ghost:"
    }

    r = requests.post(webhook_url, data=json.dumps(payload))
    if r.status_code not in range(200, 300):
        logger.error(
                "Failed to send slack {}, status={}",
                webhook_url,
                r.status_code)

def post_webhook(webhook_url, message):
    payload = {
        "message": message,
    }

    r = requests.post(webhook_url, data=json.dumps(payload))
    if r.status_code not in range(200, 300):
        logger.error(
                "Failed to send webhook {}, status={}",
                webhook_url,
                r.status_code)

