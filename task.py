from concurrent.futures import ThreadPoolExecutor

from pull_request_task import pull_request_merged_task

executor = ThreadPoolExecutor(max_workers=1)

def submit_pull_request_merged_task(payload):
    _ = executor.submit(pull_request_merged_task, payload)

