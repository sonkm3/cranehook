import hmac
import json
import logging
from hashlib import sha256
from unittest.mock import patch

from webtest import TestApp
from webtest.app import AppError

import cranehook
import settings
from src.tasks import submit_pull_request_merged_task

GITHUB_WEBHOOK_SECRET = settings.GITHUB_WEBHOOK_SECRET


def test_cranehook_webhook_ping():
    app = TestApp(cranehook.app)

    request_json = dict(id=1, value="value")

    mac = hmac.new(
        GITHUB_WEBHOOK_SECRET.encode(),
        msg=json.dumps(request_json).encode(),
        digestmod=sha256,
    )

    signature = "sha256=" + mac.hexdigest()
    headers = [("X-Hub-Signature-256", signature), ("X-GitHub-Event", "ping")]

    response = app.post_json("/", request_json, headers=headers)
    assert response.status_code == 200
    assert "pong" in response


def test_cranehook_webhook_ping_with_false_signature():
    app = TestApp(cranehook.app)

    request_json = dict(id=1, value="value")

    mac = hmac.new(
        GITHUB_WEBHOOK_SECRET.encode(),
        msg=json.dumps(request_json).encode(),
        digestmod=sha256,
    )

    signature = "sha256=" + mac.hexdigest() + "false-signature"
    headers = [("X-Hub-Signature-256", signature), ("X-GitHub-Event", "ping")]

    try:
        app.post_json("/", request_json, headers=headers)
    except AppError as e:
        assert "404" in e.args[0]


def test_cranehook_webhook_push():
    app = TestApp(cranehook.app)

    request_json = dict(id=1, value="value")

    mac = hmac.new(
        GITHUB_WEBHOOK_SECRET.encode(),
        msg=json.dumps(request_json).encode(),
        digestmod=sha256,
    )

    signature = "sha256=" + mac.hexdigest()
    headers = [("X-Hub-Signature-256", signature), ("X-GitHub-Event", "push")]

    response = app.post_json("/", request_json, headers=headers)
    assert response.status_code == 200
    assert "pong" not in response


@patch("src.tasks.submit_pull_request_merged_task")
def test_cranehook_webhook_pull_request(submit_pull_request_merged_task):
    app = TestApp(cranehook.app)

    request_json = {"action": "closed", "pull_request": {"merged": True}}

    mac = hmac.new(
        GITHUB_WEBHOOK_SECRET.encode(),
        msg=json.dumps(request_json).encode(),
        digestmod=sha256,
    )

    signature = "sha256=" + mac.hexdigest()
    headers = [("X-Hub-Signature-256", signature), ("X-GitHub-Event", "pull_request")]

    response = app.post_json("/", request_json, headers=headers)
    assert response.status_code == 200
    assert "pong" not in response


@patch("subprocess.run")
@patch("src.discord_handler.DiscordHandler.emit")
def test_cranehook_pull_request_merged_task(emit, subprocess_run):
    submit_pull_request_merged_task(None)
    emit.assert_called()


@patch("src.discord_handler.DiscordHandler.emit")
def test_discord_handler(emit):
    logger = logging.getLogger("cranehook")

    logger.error("test message")
    emit.assert_called()
