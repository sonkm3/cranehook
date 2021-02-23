import logging
from concurrent.futures import ThreadPoolExecutor
from logging import Handler

import requests

log_executor = ThreadPoolExecutor(max_workers=5)


class DiscordHandler(Handler):
    def __init__(self, webhook_url, username):
        logging.Handler.__init__(self)
        self.webhook_url = webhook_url
        self.username = username

    def mapLogRecord(self, record):
        return {"username": self.username, "content": self.format(record)}

    def emit(self, record):
        _ = log_executor.submit(
            _call_webhook, self.mapLogRecord(record), self.webhook_url
        )


def _call_webhook(payload, webhook_url):
    _ = requests.post(webhook_url, data=payload)
