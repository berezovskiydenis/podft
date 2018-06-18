from flask import render_template, make_response
from app import db
from app.errors import bp


@bp.app_errorhandler(404)
def not_found_error(error):
    response = make_response(render_template('errors/404.html'), 404)
    return response


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    response = make_response(render_template('errors/500.html'), 500)
    return response
