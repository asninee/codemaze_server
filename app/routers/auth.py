from flask_restx import Resource, Namespace, abort
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from http import HTTPStatus

from app.extensions import db
from app.models import TokenBlocklist, User
from app.api_models import user_model, login_model

authorizations = {
    "jsonWebToken": {"type": "apiKey", "in": "header", "name": "Authorization"}
}
authRouter = Namespace(
    "auth", description="`/auth` routes", authorizations=authorizations
)


@authRouter.route("/register")
class Register(Resource):
    @authRouter.expect(login_model)
    @authRouter.response(int(HTTPStatus.CREATED), "User successfully registered")
    @authRouter.response(int(HTTPStatus.CONFLICT), "Username is already registered")
    @authRouter.response(int(HTTPStatus.BAD_REQUEST), "Validation Error")
    @authRouter.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal Server Error")
    def post(self):
        """Register a new user"""
        username = authRouter.payload["username"]
        password = authRouter.payload["password"]

        if not username and password:
            abort(
                HTTPStatus.BAD_REQUEST,
                "Invalid credentials provided: Make sure to include `username`, `password`",
                status="fail",
            )

        if User.find_by_username(username=username):
            abort(
                HTTPStatus.CONFLICT,
                f"User with username {username} is already registered",
                status="fail",
            )

        user = User(
            username=username,
            password=password,
        )

        user.assign_random_avatar()

        db.session.add(user)
        db.session.commit()
        return {
            "status": "success",
            "message": "User successfully registered",
        }, HTTPStatus.CREATED


@authRouter.route("/login")
class Login(Resource):
    @authRouter.expect(login_model)
    @authRouter.response(int(HTTPStatus.OK), "Login succeeded")
    @authRouter.response(int(HTTPStatus.UNAUTHORIZED), "Incorrect login credentials")
    @authRouter.response(int(HTTPStatus.BAD_REQUEST), "User not found")
    @authRouter.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal Server Error")
    def post(self):
        """Authenticate an existing user and return an access token"""
        username = authRouter.payload["username"]
        password = authRouter.payload["password"]

        if not username and password:
            abort(
                HTTPStatus.BAD_REQUEST,
                "Invalid credentials provided: Make sure to include `username`, `password`",
                status="fail",
            )

        user = User.find_by_username(authRouter.payload["username"])

        if not user:
            abort(HTTPStatus.BAD_REQUEST, "User not found", status="fail")
        if not user.check_password(authRouter.payload["password"]):
            abort(HTTPStatus.UNAUTHORIZED, "Incorrect login credentials", status="fail")
        return {
            "status": "success",
            "message": "Login succeeded",
            "username": user.username,
            "access_token": create_access_token(identity=user, expires_delta=False),
            "token_type": "bearer",
        }, HTTPStatus.OK


@authRouter.route("/logout")
class Logout(Resource):
    method_decorators = [jwt_required()]

    @authRouter.doc(security="jsonWebToken")
    @authRouter.response(
        int(HTTPStatus.OK), "Log out succeeded, token is no longer valid"
    )
    @authRouter.response(int(HTTPStatus.BAD_REQUEST), "Validation Error")
    @authRouter.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired")
    @authRouter.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal Server Error")
    def post(self):
        """Log out a currently logged-in user and add their access token to the blocklist"""
        jti = get_jwt()["jti"]
        db.session.add(TokenBlocklist(jti=jti))
        db.session.commit()
        response_dict = dict(status="success", message="Successfully logged out")
        return response_dict, HTTPStatus.OK
