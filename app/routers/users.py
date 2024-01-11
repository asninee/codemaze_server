from flask_restx import Resource, Namespace
from flask_jwt_extended import create_access_token, get_jwt, jwt_required

from app.extensions import db
from app.models import TokenBlocklist, User
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
                password=userRouter.payload["password"],
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
        if not user.check_password(userRouter.payload["password"]):
            return {"error": "Incorrect login credentials"}, 403
        return {
            "access_token": create_access_token(user, expires_delta=False),
        }


@userRouter.route("/logout")
class Logout(Resource):
    method_decorators = [jwt_required()]

    @userRouter.doc(security="jsonWebToken")
    def post(self):
        jti = get_jwt()["jti"]
        db.session.add(TokenBlocklist(jti=jti))
        db.session.commit()
        return "Logged Out", 204
