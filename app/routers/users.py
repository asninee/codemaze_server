from flask_restx import Resource, Namespace
from flask_jwt_extended import create_access_token, current_user, get_jwt, jwt_required

from app.extensions import db
from app.models import User
from app.api_models import user_profile_model

authorizations = {
    "jsonWebToken": {"type": "apiKey", "in": "header", "name": "Authorization"}
}
userRouter = Namespace(
    "users", description="`/users` routes", authorizations=authorizations
)


@userRouter.route("/profile")
class Profile(Resource):
    method_decorators = [jwt_required()]

    @userRouter.doc(security="jsonWebToken")
    @userRouter.marshal_with(user_profile_model)
    def get(self):
        """Get the profile information of the currently logged-in user"""
        return User.query.get(current_user.id)
