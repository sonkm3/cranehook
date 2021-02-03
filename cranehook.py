import hmac
import json

from hashlib import sha256

from bottle import Bottle, run, request, HTTPError

import task
import settings


WEBHOOK_SECRET = settings.WEBHOOK_SECRET

app = Bottle()
app.catchall = False
@app.route(path='/webhook', method='POST')
def webhook():
    signature_header = request.get_header('X-Hub-Signature-256')
    if signature_header is None:
        raise HTTPError(status=404)

    _, signature = signature_header.split('=')
    mac = hmac.new(WEBHOOK_SECRET.encode(), msg=request.body.getvalue(), digestmod=sha256)
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
            return payload["action"] == "closed" and payload["merged"] == True
        if check_pull_request_merged(payload):
            task.submit_pull_request_merged_task(payload)

if __name__ == "__main__":
    run(host='localhost', port=8080, debug=True)
