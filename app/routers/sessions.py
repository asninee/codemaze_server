from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models import Session, User
from app.api_models import (
    session_input_model,
    session_model,
    session_update_model,
    user_model,
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
    @sessionRouter.expect(session_input_model)
    @sessionRouter.marshal_with(session_model)
    def post(self):
        try:
            session = Session(problem_id=sessionRouter.payload["problem_id"])
            db.session.add(session)
            db.session.commit()
            return session, 201
        except:
            return {"error": "We could not process your request"}, 400


@sessionRouter.route("/<int:id>")
class SessionAPI(Resource):
    method_decorators = [jwt_required()]

    @sessionRouter.doc(security="jsonWebToken")
    @sessionRouter.expect(session_update_model)
    @sessionRouter.marshal_with(session_model)
    def patch(self, id):
        session = Session.query.get(id)
        user = User.query.get(sessionRouter.payload["user_id"])
        if not session:
            return {"error": "Session does not exist"}, 404
        if not user:
            return {"error": "User does not exist"}, 404

        session.users.append(user)

        db.session.commit()

        return session, 200
