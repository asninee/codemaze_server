from flask_restx import Namespace, Resource
from flask_jwt_extended import current_user, jwt_required
from sqlalchemy import func

from app.models import Problem
from app.api_models import problem_model


authorizations = {
    "jsonWebToken": {"type": "apiKey", "in": "header", "name": "Authorization"}
}
problemRouter = Namespace(
    "problems", description="`/problems` routes", authorizations=authorizations
)


@problemRouter.route("/random")
class ProblemAPI(Resource):
    method_decorators = [jwt_required()]

    @problemRouter.doc(security="jsonWebToken")
    @problemRouter.marshal_with(problem_model)
    def get(self):
        """Get a random problem with the same rank as the currently logged-in user"""
        problem = (
            Problem.query.filter_by(rank_id=current_user.rank_id)
            .order_by(func.random())
            .first()
        )
        if not problem:
            return {
                "error": "The server unfortunately ran into an error when attempting to fetch the problem"
            }, 500
        return problem, 200
