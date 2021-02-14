import logging
import subprocess

import settings

from .discord_handler import DiscordHandler

logger = logging.getLogger('cranehook')
logger.setLevel(logging.INFO)
discordHandler = DiscordHandler(settings.DISCORD_WEBHOOK_URL, 'cranehook')

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
discordHandler.setFormatter(formatter)

logger.addHandler(discordHandler)

command_dict = {
    'pull_request_merged_task': settings.PULL_REQUEST_MERGED_COMMAND
}


def pull_request_merged_task(payload):
    task_command_executer(command_dict['pull_request_merged_task'])


def task_command_executer(command_list):
    for cwd, command in command_list:
        logger.info(' '.join(command))
        _ = subprocess.run(command, cwd=cwd, capture_output=True)
        logger.info(_.returncode)
        if _.returncode != 0:
            logger.error(_.stdout)
            logger.error(_.stderr)
            break
        logger.info(_.stdout)
