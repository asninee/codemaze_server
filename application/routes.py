from application import db
from flask import request, jsonify, Blueprint
from application.models import User

users = Blueprint("users", __name__)

def format_user(user):
    return {
        "username": user.username,
        "password": user.password
    }
