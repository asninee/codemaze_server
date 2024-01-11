from flask_restx import fields

from .extensions import api

login_model = api.model(
    "LoginInput", {"username": fields.String, "password": fields.String}
)

user_model = api.model("User", {"id": fields.Integer, "username": fields.String})

rank_model = api.model(
    "Rank",
    {
        "id": fields.Integer,
        "name": fields.String,
        "min_xp": fields.Integer,
        "max_xp": fields.Integer,
    },
)

problem_model = api.model(
    "Problem",
    {
        "id": fields.Integer,
        "title": fields.String,
        "content": fields.String,
        "rank": fields.List(fields.Nested(rank_model)),
    },
)
