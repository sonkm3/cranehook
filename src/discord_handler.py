import logging
from concurrent.futures import ThreadPoolExecutor
from logging import Handler

from discord import RequestsWebhookAdapter, Webhook

log_executor = ThreadPoolExecutor(max_workers=5)


class DiscordHandler(Handler):
    def __init__(self, webhook_url, username):
        logging.Handler.__init__(self)
        self.webhook_url = webhook_url
        self.username = username

    def mapLogRecord(self, record):
        return record.__dict__

    def emit(self, record):
        _ = log_executor.submit(
            _call_webhook, self.format(record), self.webhook_url, self.username
        )


def _call_webhook(message, webhook_url, username):
    webhook_id = webhook_url.split("/")[-2]
    webhook_token = webhook_url.split("/")[-1]
    webhook = Webhook.partial(
        webhook_id, webhook_token, adapter=RequestsWebhookAdapter()
    )
    webhook.send(message, username=username)
