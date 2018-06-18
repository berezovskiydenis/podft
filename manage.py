from app import create_app, db
from app.models import User, Terrorist, Org


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Terrorist=Terrorist, Org=Org)
