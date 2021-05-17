import logging

LOG_LEVEL = logging.INFO

SERVER = "auto"
PORT = 8080
HOST = "localhost"

GITHUB_WEBHOOK_SECRET = "secret"

DISCORD_WEBHOOK_URL = ""

COMMAND_MAP = {
    "PULL_REQUEST_MERGED": [
        # ['/tmp/', ['git', 'pull', 'origin', 'main']],
        # ['/tmp/', ['make', 'publish']],
        ["/tmp/", ["ls", "-l"]],
    ]
}
