import hmac
import json
import logging

from hashlib import sha256

from bottle import Bottle, request, HTTPError

from . import tasks
import settings

GITHUB_WEBHOOK_SECRET = settings.GITHUB_WEBHOOK_SECRET

cranehook_app = Bottle()
cranehook_app.catchall = False

logger = logging.getLogger('cranehook')
logger.setLevel(logging.DEBUG)


@cranehook_app.route(path='/', method='POST')
def index():
    for key in request.headers.keys():
        logger.debug(f'{key}: {request.get_header(key)}')

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

    event = request.get_header('HTTP_X_GITHUB_EVENT')
    if not event:
        logger.error('HTTP_X_GITHUB_EVENT is not set.')
        raise HTTPError(status=404)
    elif event == 'ping':
        return 'pong'

    payload = json.loads(request.body.getvalue())
    if event == 'pull_request':
        logger.info(payload["action"])
        logger.info(payload["pull_request"]["merged"])

        def check_pull_request_merged(payload):
            return payload["action"] == "closed" \
                   and payload["pull_request"]["merged"]
        if check_pull_request_merged(payload):
            tasks.submit_pull_request_merged_task(payload)
    else:
        logger.error('event not match.')
    return
