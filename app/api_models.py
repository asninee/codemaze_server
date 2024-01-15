from attr import field
from flask_restx import fields
from sqlalchemy import Integer

from .extensions import api

login_model = api.model(
    "LoginInput",
    {
        "username": fields.String(required=True),
        "password": fields.String(required=True),
    },
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

example_model = api.model(
    "Example",
    {
        "id": fields.Integer,
        "input": fields.String,
        "output": fields.String,
        "explanation": fields.String,
    },
)

problem_model = api.model(
    "Problem",
    {
        "id": fields.Integer,
        "title": fields.String,
        "description": fields.String,
        "rank": fields.List(fields.Nested(rank_model)),
        "examples": fields.List(fields.Nested(example_model)),
    },
)


session_input_model = api.model(
    "SessionInput",
    {
        "problem_id": fields.Integer(required=True),
        "user_one_id": fields.Integer(required=True),
        "user_two_id": fields.Integer(required=True),
        "winner_id": fields.Integer(required=True),
    },
)

user_model = api.model(
    "User", {"id": fields.Integer, "username": fields.String, "xp": fields.Integer}
)

session_model = api.model(
    "Session",
    {
        "id": fields.Integer,
        "problem": fields.List(fields.Nested(problem_model)),
        "winner": fields.List(fields.Nested(user_model)),
        "users": fields.List(fields.Nested(user_model)),
    },
)

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

user_leaderboard_model = api.model(
    "UserLeaderboardEntry",
    {
        "id": fields.Integer,
        "username": fields.String,
        "xp": fields.Integer,
        "wins": fields.Integer,
        "losses": fields.Integer,
        "rank": fields.List(fields.Nested(rank_model)),
    },
)
