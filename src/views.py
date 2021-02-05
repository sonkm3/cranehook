import hmac
import json

from hashlib import sha256

from bottle import Bottle, request, HTTPError

from . import tasks
import settings

GITHUB_WEBHOOK_SECRET = settings.GITHUB_WEBHOOK_SECRET

cranehook_app = Bottle()
cranehook_app.catchall = False


@cranehook_app.route(path='/', method='POST')
def index():
    signature_header = request.get_header('X-Hub-Signature-256')
    if signature_header is None:
        raise HTTPError(status=404)

    _, signature = signature_header.split('=')
    mac = hmac.new(GITHUB_WEBHOOK_SECRET.encode(),
                   msg=request.body.getvalue(),
                   digestmod=sha256)
    if not hmac.compare_digest(mac.hexdigest(), signature):
        raise HTTPError(status=404)

    event = request.get_header('HTTP_X_GITHUB_EVENT')
    if not event:
        raise HTTPError(status=404)
    elif event == 'ping':
        return 'pong'

    payload = json.loads(request.body.getvalue())
    if event == 'pull_request':
        def check_pull_request_merged(payload):
            return payload["action"] == "closed" and payload["merged"]
        if check_pull_request_merged(payload):
            tasks.submit_pull_request_merged_task(payload)
    return
