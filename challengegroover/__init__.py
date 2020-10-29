from flask import Flask, redirect, url_for
import logging
import logging.handlers
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from datetime import datetime
from .routes import *

from .models import *

def create_app():
    # config
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder="ui/templates",
        static_folder="ui/static",
    )
    app.config.from_pyfile("config.py")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spotify.db'
    db.init_app(app)

    # logging
    handler = logging.handlers.RotatingFileHandler(
        app.config["LOG_FILE"], maxBytes=app.config["LOG_SIZE"]
    )
    handler.setLevel(app.config["LOG_LEVEL"])
    handler.setFormatter(
        logging.Formatter(
            "[%(asctime)s] %(levelname)s [%(pathname)s at %(lineno)s]: %(message)s",
            "%Y-%m-%d %H:%M:%S",
        )
    )
    app.logger.addHandler(handler)
   
    db.init_app(app)

    # routes
    with app.app_context():
        from .routes import auth, root, api

        app.register_blueprint(root)
        app.register_blueprint(auth)
        app.register_blueprint(api)
        db.create_all()  # Create sql tables for our data models

    return app
