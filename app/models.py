import random
from .extensions import db
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

session_user = db.Table(
    "user_session",
    db.Column("session_id", db.Integer, db.ForeignKey("session.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.Text)
    avatar = db.Column(db.Text)
    xp = db.Column(db.Integer)
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    rank_id = db.Column(db.ForeignKey("rank.id"))
    created_at = db.Column(db.DateTime, default=func.now())

    rank = db.relationship("Rank", back_populates="users")
    sessions = db.relationship(
        "Session", secondary=session_user, back_populates="users"
    )

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.avatar = ""
        self.xp = 0
        self.wins = 0
        self.losses = 0
        self.rank_id = 1

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def rank_up(self):
        self.rank_id += 1

    def __repr__(self):
        return f"User(username: {self.username}, xp: {self.xp})"

    def assign_random_avatar(self):
        avatars = [
            "https://api.dicebear.com/7.x/bottts-neutral/svg?seed=Pepper&radius=45&backgroundType=solid,gradientLinear",
            "https://api.dicebear.com/7.x/bottts-neutral/svg?seed=Midnight&radius=45&backgroundType=solid,gradientLinear",
            "https://api.dicebear.com/7.x/bottts-neutral/svg?seed=Mittens&radius=45&backgroundType=solid,gradientLinear",
            "https://api.dicebear.com/7.x/bottts-neutral/svg?seed=Max&radius=45&backgroundType=solid,gradientLinear",
            "https://api.dicebear.com/7.x/bottts-neutral/svg?seed=Oscar&radius=45&backgroundType=solid,gradientLinear",
            "https://api.dicebear.com/7.x/bottts-neutral/svg?seed=Sassy&radius=45&backgroundType=solid,gradientLinear",
        ]

        avatar = random.choice(avatars)
        self.avatar = avatar

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()


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
    description = db.Column(db.Text)
    rank_id = db.Column(db.ForeignKey("rank.id"))

    rank = db.relationship("Rank", back_populates="problems")
    sessions = db.relationship("Session", back_populates="problem")
    examples = db.relationship("Example", back_populates="problem")

    def __init__(self, title, description, rank_id):
        self.title = title
        self.description = description
        self.rank_id = rank_id

    def __repr__(self):
        return f"Problem(title: {self.title}, rank_id: {self.rank_id})"


class Example(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    problem_id = db.Column(db.ForeignKey("problem.id"))
    input = db.Column(db.String(250))
    output = db.Column(db.String(250))
    explanation = db.Column(db.Text)
    test_case = db.Column(db.Text)

    problem = db.relationship("Problem", back_populates="examples")

    def __init__(self, problem_id, input, output, explanation, test_case):
        self.problem_id = problem_id
        self.input = input
        self.output = output
        self.explanation = explanation
        self.test_case = test_case

    def __repr__(self):
        return f"Example(problem_id: {self.problem_id})"


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    problem_id = db.Column(db.ForeignKey("problem.id"))
    winner_id = db.Column(db.ForeignKey("user.id"))

    problem = db.relationship("Problem", back_populates="sessions")
    users = db.relationship("User", secondary=session_user, back_populates="sessions")
    winner = db.relationship("User", back_populates="sessions")

    def __init__(self, problem_id, winner_id):
        self.problem_id = problem_id
        self.winner_id = winner_id

    def __repr__(self):
        return f"Session(problem_id: {self.problem_id})"


class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=func.now())

    def __init__(self, jti):
        self.jti = jti

    def __repr__(self):
        return f"TokenBlocklist(jti: {self.jti})"
