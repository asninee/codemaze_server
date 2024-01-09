import os
from flask import Flask
from dotenv import load_dotenv

from .extensions import api, db, jwt
from .routers.users import userRouter
from .models import User

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["SQLALCHEMY_DATABASE_URI"]
    app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]

    api.init_app(app)
    db.init_app(app)
    jwt.init_app(app)

    api.add_namespace(userRouter)

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).first()

    return app
