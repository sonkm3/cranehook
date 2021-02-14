from bottle import Bottle

import settings
from src.views import cranehook_app

app = Bottle()
app.catchall = False

app.merge(cranehook_app)

if __name__ == "__main__":
    app.run(host=settings.HOST, port=settings.PORT, debug=True)
