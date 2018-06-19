from app import create_app, db
from app.models import User, Terrorist, Org

import threading
import os


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Terrorist=Terrorist, Org=Org)


def call_async_kfm(app):
    with app.app_context():
        Terrorist.init_included()
        Org.init_included()
    # Call func every 6 hours if KFM_SYNC_TIMER is not set
    threading.Timer(
            os.getenv('KFM_SYNC_TIMER', 21600), call_kfn, (app,)
        ).start()


call_async_kfm(app)
