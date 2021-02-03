import hmac
import json

from hashlib import sha256
from unittest.mock import patch

from webtest import TestApp

import cranehook
import pull_request_task

import settings

WEBHOOK_SECRET = settings.WEBHOOK_SECRET


def test_cranehook_webhook_ping():
    app = TestApp(cranehook.app)

    request_json = dict(id=1, value='value')

    mac = hmac.new(WEBHOOK_SECRET.encode(), msg=json.dumps(request_json).encode(), digestmod=sha256)

    signature = 'sha256=' + mac.hexdigest()
    headers = [('X-Hub-Signature-256', signature), ('HTTP_X_GITHUB_EVENT', 'ping')]

    response = app.post_json('/cranehook/github', request_json, headers=headers)
    assert response.status_code == 200
    assert 'pong' in response


def test_cranehook_webhook_push():
    app = TestApp(cranehook.app)

    request_json = dict(id=1, value='value')

    mac = hmac.new(WEBHOOK_SECRET.encode(), msg=json.dumps(request_json).encode(), digestmod=sha256)

    signature = 'sha256=' + mac.hexdigest()
    headers = [('X-Hub-Signature-256', signature), ('HTTP_X_GITHUB_EVENT', 'push')]

    response = app.post_json('/cranehook/github', request_json, headers=headers)
    assert response.status_code == 200
    assert 'pong' not in response


@patch('task.submit_pull_request_merged_task')
def test_cranehook_webhook_pull_request(submit_pull_request_merged_task):
    app = TestApp(cranehook.app)

    request_json = {"action": "closed", "merged": True}

    mac = hmac.new(WEBHOOK_SECRET.encode(), msg=json.dumps(request_json).encode(), digestmod=sha256)

    signature = 'sha256=' + mac.hexdigest()
    headers = [('X-Hub-Signature-256', signature), ('HTTP_X_GITHUB_EVENT', 'pull_request')]

    response = app.post_json('/cranehook/github', request_json, headers=headers)
    assert response.status_code == 200
    assert 'pong' not in response


@patch('subprocess.run')
@patch('logging.error')
@patch('logging.info')
def test_cranehook_pull_request_merged_task(logging_info, logging_error, subprocess_run):
    pull_request_task.pull_request_merged_task(None)
