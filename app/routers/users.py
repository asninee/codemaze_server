from flask_restx import Resource, Namespace
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from app.models import User
from app.api_models import user_model, login_model

authorizations = {
    "jsonWebToken": {"type": "apiKey", "in": "header", "name": "Authorization"}
}
userRouter = Namespace(
    "users", description="`/users` routes", authorizations=authorizations
)


@userRouter.route("/register")
class Register(Resource):
    @userRouter.expect(login_model)
    @userRouter.marshal_with(user_model)
    def post(self):
        try:
            user = User(
                username=userRouter.payload["username"],
                password_hash=generate_password_hash(userRouter.payload["password"]),
            )
            db.session.add(user)
            db.session.commit()
            return user, 201
        except:
            return {"error": "We could not process your request"}, 400


@userRouter.route("/login")
class Login(Resource):
    @userRouter.expect(login_model)
    def post(self):
        user = User.query.filter_by(username=userRouter.payload["username"]).first()
        if not user:
            return {"error": "User does not exist"}, 404
        if not check_password_hash(user.password_hash, userRouter.payload["password"]):
            return {"error": "Incorrect login credentials"}, 403
        return {
            "user_id": user.id,
            "access_token": create_access_token(user, expires_delta=False),
        }
