from application import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def __repr__(self):
        return f"My name is {self.username}"
