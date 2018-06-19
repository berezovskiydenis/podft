# -*- coding: utf-8 -*-

from datetime import datetime

from flask import abort, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError

from app import db
from app.main import bp
from app.main.forms import OrgForm, TerroristForm
from app.models import Log, Org, Terrorist


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    """Show main page."""

    # Terrorists data
    t_count = Terrorist.query.count()

    t_list = db.session.query(
            Terrorist
        ).order_by(
            desc(Terrorist.created)
        ).first()
    t_last_update = t_list.created

    # Organization data
    o_count = Org.query.count()

    o_list = db.session.query(
            Org
        ).order_by(
            desc(Org.created)
        ).first()
    o_last_update = o_list.created

    return render_template(
            'index.html', t_count=t_count, o_count=o_count,
            t_last_update=t_last_update.strftime('%Y-%m-%d %H:%M'),
            o_last_update=o_last_update.strftime('%Y-%m-%d %H:%M')
        )


@bp.route('/persons')
@login_required
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


@bp.route('/person/<int:id>', methods=['GET', 'POST'])
@login_required
def person(id):
    """Open and edit person information."""

    existing_person = Terrorist.query.get(id)

    if existing_person is None:
        abort(404)

    form = TerroristForm(obj=existing_person)

    if request.method == 'POST' and form.validate():
        form.populate_obj(existing_person)
        db.session.commit()
        return redirect(url_for('main.persons'))

    return render_template('edit_form.html', form=form)


@bp.route('/orgs')
@login_required
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


@bp.route('/org/<int:id>', methods=['GET', 'POST'])
@login_required
def org(id):
    """Open and edit org information."""

    existing_org = Org.query.get(id)

    if existing_org is None:
        abort(404)

    form = OrgForm(obj=existing_org)

    if request.method == 'POST' and form.validate():
        form.populate_obj(existing_org)
        db.session.commit()
        return redirect(url_for('main.orgs'))

    return render_template('edit_form.html', form=form)


@bp.route('/logs')
@login_required
def logs():
    """Show just orgs."""
    page = request.args.get('page', 1, type=int)

    logs = db.session.query(
            Log
        ).order_by(
            desc(Log.created)
        ).paginate(page, 50, False)

    next_url = url_for('main.logs', page=logs.next_num) if logs.has_next else None
    prev_url = url_for('main.logs', page=logs.prev_num) if logs.has_prev else None

    return render_template(
            'logs.html', logs=logs.items, next_url=next_url, prev_url=prev_url
        )
