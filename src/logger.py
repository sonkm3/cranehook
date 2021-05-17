import logging
from logging.handlers import QueueHandler, QueueListener
from queue import SimpleQueue

import settings
from src.discord_handler import DiscordHandler


def start_logger():
    queue = SimpleQueue()

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

    logger = logging.getLogger("cranehook")
    logger.setLevel(settings.LOG_LEVEL)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.DEBUG)

    discord_handler = DiscordHandler(settings.DISCORD_WEBHOOK_URL, "cranehook")
    discord_handler.setFormatter(formatter)
    discord_handler.setLevel(logging.INFO)
    queue_listner = QueueListener(
        queue, discord_handler, stream_handler, respect_handler_level=True
    )

    queue_handler = QueueHandler(queue)
    logger.addHandler(queue_handler)

    queue_listner.start()
