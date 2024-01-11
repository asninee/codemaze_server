import os
from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
from .extensions import api, db, jwt, socketio
from .routers.users import userRouter
from .routers.sockets import sockets
from .models import User

load_dotenv()

def create_app():
    allowed_origins = ["http://localhost:5173", "http://localhost:5174", "http://localhost:5175"]
    app = Flask(__name__)
    CORS(app, origins=allowed_origins) #change to render links eventually
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["SQLALCHEMY_DATABASE_URI"]
    app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]
    app.config["SECRET_KEY"] = "secret"

    api.init_app(app)
    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(sockets)

    # socketio.init_app(app)
    socketio.init_app(app, cors_allowed_origins=allowed_origins)  #change to render links eventually
    


    api.add_namespace(userRouter)

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).first()
    
    return app
