import datetime
import os
import threading

from sqlalchemy import inspect

from app import create_app, db
from app.models import Org, Terrorist, User

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Terrorist=Terrorist, Org=Org)


def call_async_kfm(app):
    """Async function to grab included terrorists (persons and orgs)
    from KFM web page.
    """
    with app.app_context():
        # Use and inspect method to check is tables exists
        inspector = inspect(db.engine)
        # get_table_names returns list of existing tables or empty list
        table_names = inspector.get_table_names()

        # Check if tables are in the list of existing tables
        if 'terrorists' in table_names and 'orgs' in table_names:
            Terrorist.init_included()
            Org.init_included()

        # Call func every 6 hours if KFM_SYNC_TIMER is not set
        t = threading.Timer(
                int(os.getenv('KFM_SYNC_TIMER', 21600)), call_async_kfm, (app,)
            )
        t.daemon = True
        t.start()

try:
    call_async_kfm(app)
except (KeyboardInterrupt, SystemExit):
    print('\nReceived keyboard interrupt, quitting threads.\n')

db.get_tables_for_bind()
