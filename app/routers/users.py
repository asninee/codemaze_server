from flask_restx import Resource, Namespace, abort
from flask_jwt_extended import current_user, jwt_required
from http import HTTPStatus


from app.extensions import db
from app.models import User
from app.api_models import (
    user_profile_model,
    user_leaderboard_model,
    user_avatar_model,
    user_avatar_update_model,
    user_avatar_fetch_model,
)

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
    @userRouter.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired")
    @userRouter.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal Server Error")
    @userRouter.marshal_with(user_profile_model)
    def get(self):
        """Get the profile information of the currently logged-in user"""
        return User.query.get(current_user.id), 200


@userRouter.route("/leaderboard")
class Leaderboard(Resource):
    method_decorators = [jwt_required()]

    @userRouter.doc(security="jsonWebToken")
    @userRouter.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired")
    @userRouter.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal Server Error")
    @userRouter.marshal_list_with(user_leaderboard_model)
    def get(self):
        """Get all users, ordered by their xp"""
        return User.query.order_by(User.xp.desc()).all(), 200


@userRouter.route("/update")
class UpdateAvatar(Resource):
    method_decorators = [jwt_required()]

    @userRouter.doc(security="jsonWebToken")
    @userRouter.response(int(HTTPStatus.BAD_REQUEST), "Validation Error")
    @userRouter.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired")
    @userRouter.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal Server Error")
    @userRouter.expect(user_avatar_update_model)
    @userRouter.marshal_with(user_avatar_model)
    def patch(self):
        """Update the currently logged-in user's avatar"""
        current_user.avatar = userRouter.payload["avatar"]
        db.session.commit()
        return current_user, 200


@userRouter.route("/avatars")
class GetAvatars(Resource):
    method_decorators = [jwt_required()]

    @userRouter.doc(security="jsonWebToken")
    @userRouter.response(int(HTTPStatus.BAD_REQUEST), "Users not found")
    @userRouter.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired")
    @userRouter.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal Server Error")
    @userRouter.expect(user_avatar_fetch_model)
    @userRouter.marshal_list_with(user_avatar_model)
    def post(self):
        """Get the avatars of two users based on their usernames"""
        users = User.query.filter(
            (User.username == userRouter.payload["username_one"])
            | (User.username == userRouter.payload["username_two"])
        ).all()

        if not users:
            abort(HTTPStatus.BAD_REQUEST, "Users not found", status="fail")
        return users, 200
