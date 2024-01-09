from flask_restx import fields

from .extensions import api

login_model = api.model(
    "LoginInput", {"username": fields.String, "password": fields.String}
)

user_model = api.model("User", {"id": fields.Integer, "username": fields.String})
