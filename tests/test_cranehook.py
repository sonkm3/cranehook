import hmac
import json

from hashlib import sha256
from unittest.mock import patch

from webtest import TestApp

import cranehook
from src.tasks import submit_pull_request_merged_task

import settings

GITHUB_WEBHOOK_SECRET = settings.GITHUB_WEBHOOK_SECRET


def test_cranehook_webhook_ping():
    app = TestApp(cranehook.app)

    request_json = dict(id=1, value='value')

    mac = hmac.new(GITHUB_WEBHOOK_SECRET.encode(),
                   msg=json.dumps(request_json).encode(),
                   digestmod=sha256)

    signature = 'sha256=' + mac.hexdigest()
    headers = [('X-Hub-Signature-256', signature),
               ('X-GitHub-Event', 'ping')]

    response = app.post_json('/', request_json, headers=headers)
    assert response.status_code == 200
    assert 'pong' in response


def test_cranehook_webhook_push():
    app = TestApp(cranehook.app)

    request_json = dict(id=1, value='value')

    mac = hmac.new(GITHUB_WEBHOOK_SECRET.encode(),
                   msg=json.dumps(request_json).encode(),
                   digestmod=sha256)

    signature = 'sha256=' + mac.hexdigest()
    headers = [('X-Hub-Signature-256', signature),
               ('X-GitHub-Event', 'push')]

    response = app.post_json('/', request_json, headers=headers)
    assert response.status_code == 200
    assert 'pong' not in response


@patch('src.tasks.submit_pull_request_merged_task')
def test_cranehook_webhook_pull_request(submit_pull_request_merged_task):
    app = TestApp(cranehook.app)

    request_json = {"action": "closed", "pull_request": {"merged": True}}

    mac = hmac.new(GITHUB_WEBHOOK_SECRET.encode(),
                   msg=json.dumps(request_json).encode(),
                   digestmod=sha256)

    signature = 'sha256=' + mac.hexdigest()
    headers = [('X-Hub-Signature-256', signature),
               ('X-GitHub-Event', 'pull_request')]

    response = app.post_json('/', request_json, headers=headers)
    assert response.status_code == 200
    assert 'pong' not in response


@patch('subprocess.run')
@patch('src.discord_handler._call_webhook')
def test_cranehook_pull_request_merged_task(_call_webhook,
                                            subprocess_run):
    submit_pull_request_merged_task(None)
