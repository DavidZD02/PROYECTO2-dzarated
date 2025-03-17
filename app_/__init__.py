from flask import Flask
from app_.config.db import db
from app_.config.routes import register_routes


def create_app(config):
    app = Flask(__name__, template_folder="views")

    app.config.from_object(config)
    db.init_app(app)
    register_routes(app)

    with app.app_context():
        db.create_all()

    return app
