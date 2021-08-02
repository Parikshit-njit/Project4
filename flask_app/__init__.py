from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_app.routes import routes_api



db = SQLAlchemy()


def create_app():
    """Construct the core application."""
    app = Flask(__name__,
                instance_relative_config=False,
                template_folder="templates",
                static_folder="static"
                )

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///addresses.db'
    app.config['SECRET_KEY'] = "Hello World!"

    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')
    app.register_blueprint(routes_api)

    db.init_app(app)

    with app.app_context():
        from . import routes
        return app

import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))
