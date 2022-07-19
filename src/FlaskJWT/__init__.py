""" Flask app intialization and facty method """

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from FlaskJWT.config import getConfig

cors = CORS()
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app(congifName):
    app = Flask("Flask-JWT-Authentication")
    app.config.from_object(getConfig(congifName))

    from FlaskJWT.api import apiBp

    app.register_blueprint(apiBp)

    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    return app
