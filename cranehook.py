import logging
from logging.handlers import QueueHandler, QueueListener
from queue import SimpleQueue

from bottle import Bottle

import settings
from src.discord_handler import DiscordHandler
from src.views import cranehook_app

queue = SimpleQueue()

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger = logging.getLogger("cranehook")
logger.setLevel(settings.LOG_LEVEL)

discord_handler = DiscordHandler(settings.DISCORD_WEBHOOK_URL, "cranehook")
discord_handler.setFormatter(formatter)
# logger.addHandler(discord_handler)
queue_listner = QueueListener(queue, discord_handler, respect_handler_level=True)

queue_handler = QueueHandler(queue)
logger.addHandler(queue_handler)

queue_listner.start()

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


app = Bottle()
app.catchall = False

app.merge(cranehook_app)

if __name__ == "__main__":
    app.run(host=settings.HOST, port=settings.PORT, debug=True, server=settings.SERVER)
