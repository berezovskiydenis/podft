# -*- coding: utf-8 -*-
from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    login.init_app(app)

    # Authentication blueprint
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Errors blueprint
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    # Main blueprint
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # API blueprint
    from app.api_v1 import bp as api_v1_bp
    app.register_blueprint(api_v1_bp, url_prefix='/api/v1')

    return app


# from app import models
