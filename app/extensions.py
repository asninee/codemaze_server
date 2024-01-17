from flask_cors import CORS
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO


api = Api(
    title="Codemaze API",
    description="Interact with the Codemaze API through the routes below",
)
db = SQLAlchemy()
jwt = JWTManager()
socketio = SocketIO()
cors = CORS()
