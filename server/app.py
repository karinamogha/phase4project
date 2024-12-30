#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import Flask, jsonify, request, session
from flask_restful import Resource, Api
from flask_bcrypt import Bcrypt
from flask_cors import CORS

# Local imports
from config import app, api, db
from models import User, Category, Expense

# Initialize extensions
bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True)

# Resources
class UserList(Resource):
    def get(self):
        users = User.query.all()
        return [user.to_dict() for user in users], 200

    def post(self):
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            return {"error": "Username, email, and password are required"}, 400

        # Check if username or email already exists
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            return {"error": "Username or email already exists"}, 400

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return new_user.to_dict(), 201


class UserDetail(Resource):
    def get(self, id):
        user = User.query.get(id)
        if not user:
            return {"error": "User not found"}, 404
        return user.to_dict(), 200


class ExpenseList(Resource):
    def get(self):
        # Check if the user is logged in
        if "user_id" not in session:
            return {"error": "Unauthorized"}, 401

        # Fetch expenses only for the logged-in user
        user_id = session["user_id"]
        expenses = Expense.query.filter_by(user_id=user_id).all()
        return [expense.to_dict() for expense in expenses], 200

    def post(self):
        user_id = session.get("user_id")  # Ensure the user is logged in
        if not user_id:
            return {"error": "Unauthorized. Please log in."}, 401

        data = request.get_json()
        name = data.get("name")
        amount = data.get("amount")
        date = data.get("date")
        category_id = data.get("category_id")

        if not name or not amount or not date:
            return {"error": "Name, amount, and date are required"}, 400

        new_expense = Expense(
            name=name,
            amount=amount,
            date=date,
            user_id=user_id,
            category_id=category_id,
        )
        db.session.add(new_expense)
        db.session.commit()
        return new_expense.to_dict(), 201


class ExpenseDetail(Resource):
    def get(self, id):
        # Ensure user is logged in
        user_id = session.get("user_id")
        if not user_id:
            return {"error": "Unauthorized. Please log in."}, 401

        # Fetch the expense and ensure it belongs to the user
        expense = Expense.query.filter_by(id=id, user_id=user_id).first()
        if not expense:
            return {"error": "Expense not found or unauthorized access"}, 404
        return expense.to_dict(), 200


class CategoryList(Resource):
    def get(self):
        categories = Category.query.all()
        return [category.to_dict() for category in categories], 200

    def post(self):
        data = request.get_json()
        name = data.get("name")

        if not name:
            return {"error": "Category name is required"}, 400

        if Category.query.filter_by(name=name).first():
            return {"error": "Category already exists"}, 400

        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()
        return new_category.to_dict(), 201


class CategoryDetail(Resource):
    def get(self, id):
        category = Category.query.get(id)
        if not category:
            return {"error": "Category not found"}, 404
        return category.to_dict(), 200


# Register route
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password are required"}), 400

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"error": "Username or email already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully", "user": new_user.to_dict()}), 201


# Login route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    user = User.query.filter_by(username=data.get("username")).first()
    if user and bcrypt.check_password_hash(user.password, data.get("password")):
        session["user_id"] = user.id
        session["username"] = user.username
        return jsonify({"message": "Login successful", "user_id": user.id}), 200

    return jsonify({"error": "Invalid credentials"}), 401


# Logout route
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
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
