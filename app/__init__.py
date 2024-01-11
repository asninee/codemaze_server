import os
from flask import Flask
from dotenv import load_dotenv
from .extensions import api, db, jwt, socketio
from .seed import initialize_db
from .routers.users import userRouter
from .routers.sockets import socketRouter
from .routers.problems import problemRouter
from .routers.sessions import sessionRouter
from .models import TokenBlocklist, User

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["SQLALCHEMY_DATABASE_URI"]
    app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]

    api.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app)

    api.add_namespace(userRouter)
    api.add_namespace(socketRouter)
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

    @socketio.on("message")
    def handle_message(msg):
        print("Received message: " + msg)
        socketio.emit("Message", msg, broadcast=True)

    initialize_db(app, db)

    return app
