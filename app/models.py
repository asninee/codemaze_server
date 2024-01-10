from .extensions import db
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(250))
    xp = db.Column(db.Integer)
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    rank_id = db.Column(db.ForeignKey("rank.id"))
    created_at = db.mapped_column(db.DateTime, default=func.now())

    rank = db.relationship("Rank", back_populates="users")

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.xp = 0
        self.wins = 0
        self.losses = 0
        self.rank_id = 1

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return f"User(username: {self.username}, xp: {self.xp})"


class Rank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    min_xp = db.Column(db.Integer)
    max_xp = db.Column(db.Integer)

    users = db.relationship("User", back_populates="rank")
    problems = db.relationship("Problem", back_populates="rank")

    def __init__(self, name, min_xp, max_xp):
        self.name = name
        self.min_xp = min_xp
        self.max_xp = max_xp

    def __repr__(self):
        return f"Rank(name: {self.name}, min_xp: {self.min_xp}, max_xp: {self.max_xp})"


class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True)
    content = db.Column(db.String(1000))
    rank_id = db.Column(db.ForeignKey("rank.id"))

    rank = db.relationship("Rank", back_populates="problems")

    def __init__(self, title, content, rank_id):
        self.title = title
        self.content = content
        self.rank_id = rank_id

    def __repr__(self):
        return f"Problem(title: {self.title}, rank_id: {self.rank_id})"
