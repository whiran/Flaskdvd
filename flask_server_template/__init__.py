from flask import Flask
import logging
import os

from db.db_extensions import db_obj
from flask_routes import routes

log = logging.getLogger('pythonLogger') # This handler comes from config>logger.conf
# https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/

def create_app(flask_config=None):
    """Construct the core application."""
    log.info(flask_config)
    app = Flask(__name__, instance_relative_config=False)

    if flask_config is None:
        app.config['DEBUG'] = False
        if 'SQLALCHEMY_DATABASE_URI' not in os.environ:
            raise RuntimeError('Environment variables not set')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_ECHO'] = False
    else:
        app.config.from_object(flask_config)

    db_obj.init_app(app)

    app.register_blueprint(routes)
    return app
