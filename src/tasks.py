from concurrent.futures import ThreadPoolExecutor

from .task_command import pull_request_merged_task

executor = ThreadPoolExecutor(max_workers=1)

def submit_pull_request_merged_task(payload):
    _ = executor.submit(pull_request_merged_task, payload)

