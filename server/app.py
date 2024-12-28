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

bcrypt = Bcrypt(app)
CORS(app)

# Resources
class UserList(Resource):
    def get(self):
        users = User.query.all()
        return [user.to_dict() for user in users], 200

    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return {"error": "Username and password are required"}, 400

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        new_user = User(username=username, password=hashed_password)
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
        expenses = Expense.query.all()
        return [expense.to_dict() for expense in expenses], 200

    def post(self):
        data = request.get_json()
        name = data.get("name")
        amount = data.get("amount")
        date = data.get("date")
        user_id = data.get("user_id")
        category_id = data.get("category_id")

        if not name or not amount or not date or not user_id:
            return {"error": "Name, amount, date, and user_id are required"}, 400

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
        expense = Expense.query.get(id)
        if not expense:
            return {"error": "Expense not found"}, 404
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
    