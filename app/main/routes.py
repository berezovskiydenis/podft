# -*- coding: utf-8 -*-

from datetime import datetime

from flask import abort, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError

from app import db
from app.main import bp
from app.models import Org, Terrorist


@bp.route('/')
@bp.route('/index')
def index():
    """Show main page."""
    # Terrorists data
    t_count = Terrorist.query.count()
    # Organization data
    o_count = Org.query.count()

    return render_template('index.html', t_count=t_count, o_count=o_count)


@bp.route('/persons')
def persons():
    """Show just persons."""

    page = request.args.get('page', 1, type=int)

    ters = db.session.query(
            Terrorist
        ).order_by(
            desc(Terrorist.created)
        ).paginate(page, 30, False)

    next_url = url_for('main.persons', page=ters.next_num) if ters.has_next else None
    prev_url = url_for('main.persons', page=ters.prev_num) if ters.has_prev else None

    return render_template(
            'persons.html', ters=ters.items, next_url=next_url,
            prev_url=prev_url
        )


@bp.route('/orgs')
def orgs():
    """Show just orgs."""
    page = request.args.get('page', 1, type=int)

    orgs = db.session.query(
            Org
        ).order_by(
            desc(Org.created)
        ).paginate(page, 30, False)

    next_url = url_for('main.orgs', page=orgs.next_num) if orgs.has_next else None
    prev_url = url_for('main.orgs', page=orgs.prev_num) if orgs.has_prev else None

    return render_template(
            'orgs.html', orgs=orgs.items, next_url=next_url, prev_url=prev_url
        )
