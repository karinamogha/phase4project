# Standard library imports
import os
if not os.path.exists("instance"):
    os.makedirs("instance")

# Remote library imports
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# Instantiate app, set attributes
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///instance/app.db')  # Correct database location
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key_here')  # Use environment variable or default secret key
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///instance/app.db')
app.config['JSON_SORT_KEYS'] = False  # Disable JSON key sorting for better readability
app.json.compact = False

# Define metadata, instantiate db
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(app, metadata=metadata)  # Single `db` instance
migrate = Migrate(app, db)  # Properly registers `db` with the Flask app
#db.init_app(app) # Unnecessary, as `Migrate` handles this

# Instantiate REST API
api = Api(app)

# Instantiate CORS
CORS(app)
