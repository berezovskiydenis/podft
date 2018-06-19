from app import create_app, db
from app.models import User, Terrorist, Org

import threading
import os

import datetime

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Terrorist=Terrorist, Org=Org)


def call_async_kfm(app):

    dif = datetime.datetime.utcnow() - app_start
    if dif.seconds > 1000:

        with app.app_context():
            Terrorist.init_included()
            Org.init_included()

        # Call func every 6 hours if KFM_SYNC_TIMER is not set
        t = threading.Timer(
                int(os.getenv('KFM_SYNC_TIMER', 21600)), call_async_kfm, (app,)
            )
        t.daemon = True
        t.start()

app_start = datetime.datetime.utcnow()

try:
    call_async_kfm(app)
except (KeyboardInterrupt, SystemExit):
    print('\nReceived keyboard interrupt, quitting threads.\n')
