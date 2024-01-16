from http import HTTPStatus
from flask import abort
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models import Session, User
from app.api_models import (
    session_input_model,
    session_model,
)


authorizations = {
    "jsonWebToken": {"type": "apiKey", "in": "header", "name": "Authorization"}
}
sessionRouter = Namespace(
    "sessions", description="`/sessions` routes", authorizations=authorizations
)


@sessionRouter.route("")
class SessionsAPI(Resource):
    method_decorators = [jwt_required()]

    @sessionRouter.doc(security="jsonWebToken")
    @sessionRouter.response(int(HTTPStatus.BAD_REQUEST), "Validation Error")
    @sessionRouter.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired")
    @sessionRouter.response(
        int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal Server Error"
    )
    @sessionRouter.expect(session_input_model)
    @sessionRouter.marshal_with(session_model)
    def post(self):
        """Create a new session with a related problem, participants, and a winner assigned to it"""
        user1 = User.query.get(sessionRouter.payload["user_one_id"])
        user2 = User.query.get(sessionRouter.payload["user_two_id"])
        winner = User.query.get(sessionRouter.payload["winner_id"])

        if not user1 and user2 and winner:
            abort(
                HTTPStatus.BAD_REQUEST,
                "Invalid credentials provided",
                status="fail",
            )

        session = Session(
            problem_id=sessionRouter.payload["problem_id"], winner_id=winner.id
        )

        db.session.add(session)
        session.users.append(user1)
        session.users.append(user2)

        winner.xp += 10
        winner.wins += 1

        if winner.id != user1.id:
            loser = user1
        else:
            loser = user2

        loser.losses += 1

        if winner.xp > winner.rank.max_xp:
            winner.rank_up()

        db.session.commit()
        return session, 201
