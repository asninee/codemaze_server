import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from .extensions import api, db, jwt, socketio
from .seed import initialize_db
from .routers.users import userRouter
from .routers.sockets import sockets
from .routers.problems import problemRouter
from .routers.sessions import sessionRouter
from .models import TokenBlocklist, User

load_dotenv()


def create_app():
    allowed_origins = [
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
    ]
    app = Flask(__name__)
    CORS(app, origins=allowed_origins)  # change to render links eventually
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["SQLALCHEMY_DATABASE_URI"]
    app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]
    app.config["SECRET_KEY"] = "secret"

    api.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    socketio.init_app(
        app, cors_allowed_origins=allowed_origins
    )  # change to render links eventually

    app.register_blueprint(sockets)
    api.add_namespace(userRouter)
    api.add_namespace(problemRouter)
    api.add_namespace(sessionRouter)

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(_jwt_header, jwt_payload: dict) -> bool:
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

        return token is not None

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).first()

    initialize_db(app, db)

    return app
