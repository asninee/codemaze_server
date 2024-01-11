from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required


authorizations = {
    "jsonWebToken": {"type": "apiKey", "in": "header", "name": "Authorization"}
}
socketsRouter = Namespace(
    "sockets", description="`/sockets` routes", authorizations=authorizations
)


@socketsRouter.route("")
class SocketsAPI(Resource):
    method_decorators = [jwt_required()]

    @socketsRouter.doc(security="jsonWebToken")
    def get(self):
        return "test123", 200
