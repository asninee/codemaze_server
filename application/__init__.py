from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

#Defining db
db = SQLAlchemy()
        
# Application factory
def create_app(env=None):
    # Initialisation of the app
    app = Flask(__name__)
    
    # Set up the environment variables depending on the environment
    if env == 'TEST':
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    else:
        app.config['TESTING'] = False
        app.config['DEBUG'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
    
    # Connection of the db to the app
    db.init_app(app)

    # Making sure db is created in an application context
    app.app_context().push()
    from application.models import User
    db.create_all()
    CORS(app)
    
    from application.routes import users
    app.register_blueprint(users)

    return app
    