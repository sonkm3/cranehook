import hmac
import json
import logging
from hashlib import sha256

from bottle import Bottle, HTTPError, request

import settings

from . import tasks

GITHUB_WEBHOOK_SECRET = settings.GITHUB_WEBHOOK_SECRET

cranehook_app = Bottle()
cranehook_app.catchall = True

logger = logging.getLogger('cranehook')
logger.setLevel(logging.INFO)


def require_signature(func):
    def check_signature(**kwargs):
        signature_header = request.get_header('X-Hub-Signature-256')
        if signature_header is None:
            logger.error('signature is not set.')
            raise HTTPError(status=404)

        _, signature = signature_header.split('=')

        mac = hmac.new(GITHUB_WEBHOOK_SECRET.encode(),
                       msg=request.body.getvalue(),
                       digestmod=sha256)

        if not hmac.compare_digest(mac.hexdigest(), signature):
            logger.error('signature does not match.')
            raise HTTPError(status=404)
        return func(**kwargs)

    return check_signature


def require_event(func):
    def check_event(**kwargs):
        event = request.get_header('X-GitHub-Event')
        if not event:
            logger.error('X-GitHub-Event is not set.')
            raise HTTPError(status=404)
        return func(**kwargs)

    return check_event


@cranehook_app.route(path='/', method='POST')
@require_signature
@require_event
def index():
    for key in request.headers.keys():
        logger.debug(f'{key}: {request.get_header(key)}')

    event = request.get_header('X-GitHub-Event')
    logger.info(event)

    payload = json.loads(request.body.getvalue())
    if 'action' in payload:
        logger.info(payload["action"])

    if event == 'pull_request':

        def check_pull_request_merged(payload):
            return payload["action"] == "closed" \
                   and payload["pull_request"]["merged"]
        if check_pull_request_merged(payload):
            tasks.submit_pull_request_merged_task(payload)
    elif event == 'ping':
        return 'pong'
    else:
        logger.error('event not match.')
    return
