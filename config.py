import os
from dotenv import load_dotenv


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'the_most_secure')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        default='sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelomentConfig(Config):
    FLASK_ENV = 'development'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        default='sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    )


config = {
    'development': DevelomentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelomentConfig
}
