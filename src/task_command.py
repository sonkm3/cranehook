import logging
import subprocess

import settings

logger = logging.getLogger("cranehook")

command_dict = {"pull_request_merged_task": settings.PULL_REQUEST_MERGED_COMMAND}


def pull_request_merged_task(payload):
    task_command_executer(command_dict["pull_request_merged_task"])


def task_command_executer(command_list):
    for cwd, command in command_list:
        logger.info(" ".join(command))
        _ = subprocess.run(command, cwd=cwd, capture_output=True)
        logger.info(f"return code: {_.returncode}")
        if _.returncode != 0:
            logger.error(f"stdout: {_.stdout}")
            logger.error(f"stderr: {_.stderr}")
            break
        logger.info(f"stdout: {_.stdout}")
