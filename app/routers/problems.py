from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from sqlalchemy import func

from app.models import Problem
from app.api_models import problem_model


authorizations = {
    "jsonWebToken": {"type": "apiKey", "in": "header", "name": "Authorization"}
}
problemRouter = Namespace(
    "problems", description="`/problems` routes", authorizations=authorizations
)


@problemRouter.route("")
class ProblemAPI(Resource):
    method_decorators = [jwt_required()]

    @problemRouter.doc(security="jsonWebToken")
    @problemRouter.marshal_with(problem_model)
    def get(self):
        problem = Problem.query.order_by(func.random()).first()
        if not problem:
            return {
                "error": "The server unfortunately ran into an error when attempting to fetch the problem"
            }, 500
        return problem, 200
