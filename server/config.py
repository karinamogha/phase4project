import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from sqlalchemy import MetaData
from flask_cors import CORS

# App initialization
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'supersecretkey')

# SQLAlchemy setup
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(app, metadata=metadata)  # Pass `app` to `SQLAlchemy` here

# Migrate and API
migrate = Migrate(app, db)  # Ensure `app` and `db` are passed here
api = Api(app)

# CORS setup
CORS(app)