from flask_restx import fields

from .extensions import api

login_model = api.model(
    "LoginInput", {"username": fields.String, "password": fields.String}
)

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

session_model = api.model(
    "Session",
    {
        "id": fields.Integer,
        "problem": fields.List(fields.Nested(problem_model)),
        # "users": fields.List(fields.Nested(user_model)),
    },
)

session_input_model = api.model("SessionInput", {"problem_id": fields.Integer})

session_update_model = api.model(
    "SessionUpdate",
    {"user_id": fields.Integer},
)

user_model = api.model("User", {"id": fields.Integer, "username": fields.String})

user_profile_model = api.model(
    "UserProfile",
    {
        "id": fields.Integer,
        "username": fields.String,
        "xp": fields.Integer,
        "wins": fields.Integer,
        "losses": fields.Integer,
        "rank": fields.List(fields.Nested(rank_model)),
        "sessions": fields.List(fields.Nested(session_model)),
    },
)
