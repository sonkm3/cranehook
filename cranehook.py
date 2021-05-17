from bottle import Bottle

import settings
from src.views import cranehook_app
from src.logger import start_logger

start_logger()

app = Bottle()
app.catchall = False

app.merge(cranehook_app)

if __name__ == "__main__":
    app.run(host=settings.HOST, port=settings.PORT, debug=True, server=settings.SERVER)
