#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import Flask, jsonify, request, session
from flask_restful import Resource, Api
from flask_bcrypt import Bcrypt
from flask_cors import CORS

# Local imports
from config import app, api

bcrypt = Bcrypt(app)
CORS(app)

# Placeholder Resources
class UserList(Resource):
    def get(self):
        # Placeholder user data
        return {
            "users": [
                {"id": 1, "username": "john_doe", "email": "john@example.com"},
                {"id": 2, "username": "jane_smith", "email": "jane@example.com"},
            ]
        }

class UserDetail(Resource):
    def get(self, id):
        # Placeholder for fetching a single user
        return {"id": id, "username": "john_doe", "email": "john@example.com"}

class ExpenseList(Resource):
    def get(self):
        # Placeholder expense data
        return {
            "expenses": [
                {"id": 1, "description": "Rent", "amount": 1200.0, "date": "2024-12-01", "user_id": 1, "category_id": 1},
                {"id": 2, "description": "Groceries", "amount": 150.0, "date": "2024-12-02", "user_id": 2, "category_id": 2},
            ]
        }

class ExpenseDetail(Resource):
    def get(self, id):
        # Placeholder for fetching a single expense
        return {"id": id, "description": "Rent", "amount": 1200.0, "date": "2024-12-01", "user_id": 1, "category_id": 1}

class CategoryList(Resource):
    def get(self):
        # Placeholder category data
        return {
            "categories": [
                {"id": 1, "name": "Rent"},
                {"id": 2, "name": "Groceries"},
            ]
        }

class CategoryDetail(Resource):
    def get(self, id):
        # Placeholder for fetching a single category
        return {"id": id, "name": "Rent"}

# Login route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Placeholder for user validation
    user = {"email": "john@example.com", "password": bcrypt.generate_password_hash("password123").decode("utf-8")}

    if data['email'] == user['email'] and bcrypt.check_password_hash(user['password'], data['password']):
        session['user_id'] = 1  # Replace with actual user ID from database
        session['user_email'] = data['email']
        return jsonify({"message": "Login successful", "user_id": 1})
    
    return jsonify({"error": "Invalid credentials"}), 401

# Logout route
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Clear all session data
    return jsonify({"message": "Logout successful"})

# Error Handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": "Internal server error"}), 500

# Add resources to the API
api.add_resource(UserList, '/users')
api.add_resource(UserDetail, '/users/<int:id>')
api.add_resource(ExpenseList, '/expenses')
api.add_resource(ExpenseDetail, '/expenses/<int:id>')
api.add_resource(CategoryList, '/categories')
api.add_resource(CategoryDetail, '/categories/<int:id>')

# Default route
@app.route('/')
def index():
    return '<h1>Project Server</h1>'

if __name__ == '__main__':
    app.run(port=5555, debug=True)
    