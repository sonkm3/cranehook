import urllib
from concurrent.futures import ThreadPoolExecutor
from logging.handlers import HTTPHandler

log_executor = ThreadPoolExecutor(max_workers=5)


class DiscordHandler(HTTPHandler):
    def __init__(self, webhook_url, username):
        webhook = urllib.parse.urlparse(webhook_url)
        super().__init__(webhook[1], webhook[2], method="POST", secure=True)
        self.webhook_url = webhook_url
        self.username = username

    def mapLogRecord(self, record):
        return {"username": self.username, "content": self.format(record)}
