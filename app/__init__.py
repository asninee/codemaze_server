import os
from flask import Flask
from dotenv import load_dotenv

from .extensions import api, db, jwt

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["SQLALCHEMY_DATABASE_URI"]
    app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]

    api.init_app(app)
    db.init_app(app)
    jwt.init_app(app)

    return app
