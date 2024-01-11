from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required


authorizations = {
    "jsonWebToken": {"type": "apiKey", "in": "header", "name": "Authorization"}
}
socketRouter = Namespace(
    "sockets", description="`/sockets` routes", authorizations=authorizations
)


@socketRouter.route("")
class SocketsAPI(Resource):
    method_decorators = [jwt_required()]

    @socketRouter.doc(security="jsonWebToken")
    def get(self):
        return "test123", 200
