# -*- coding: utf-8 -*-
from app import db
from app.models import Terrorist, Org
from app.api_v1 import bp
from app.api_v1.errors import error_response, bad_request

from flask import jsonify, request, url_for, render_template
from sqlalchemy import or_


@bp.route('/org', methods=['GET'])
def org():
    # Get request parameters and check if 'name' is presented
    data = request.args

    if 'name' not in data:
        return bad_request('Parameter name must be in request')

    org_found = db.session.query(Org).filter(
            or_(
                Org.name_eng == data['name'],
                Org.name == data['name']
            )

        ).first()

    if org_found:
        result = [org_found.as_json()]
        return jsonify(result)
    else:
        return error_response(404, 'Organization not found')


@bp.route('/terrorist', methods=['GET'])
def terrorist():

    data = request.args

    if 'iin' in data:
        ter = db.session.query(
            Terrorist
        ).filter(
            Terrorist.iin == data['iin'].strip()
        ).first()
    elif 'lname' in data and 'fname' in data:
        ter = db.session.query(
                Terrorist
            ).filter(
                Terrorist.lname == data['lname'].strip().upper(),
                Terrorist.fname == data['fname'].strip().upper()
            ).first()
    else:
        return bad_request(
                'parameters iin or lname and fname must be in request'
            )

    if ter:
        response = jsonify([ter.as_json()])
        return response

    return error_response(404)


@bp.route('/doc')
def api_doc():
    endpoint_o = url_for('api.org', _external=True)
    endpoint_t = url_for('api.terrorist', _external=True)
    return render_template('api_doc.html', epo=endpoint_o, ept=endpoint_t)
