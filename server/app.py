#!/usr/bin/env python3

from server.config import app, api, db
from server.models import User, Category, Expense
from flask import jsonify, request, session
from flask_restful import Resource
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from datetime import datetime

bcrypt = Bcrypt(app)
CORS(app)

class UserList(Resource):
    def get(self):
        users = User.query.all()
        return [user.to_dict() for user in users], 200

    def post(self):
        data = request.get_json()
        if not data.get("username") or not data.get("password"):
            return {"error": "Username and password are required"}, 400

        new_user = User(
            username=data["username"],
            password=data["password"]
        )
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
        if not data.get("name") or not data.get("amount") or not data.get("date") or not data.get("user_id"):
            return {"error": "Name, amount, date, and user_id are required"}, 400

        try:
            date = datetime.strptime(data["date"], "%Y-%m-%d").date()
        except ValueError:
            return {"error": "Invalid date format. Use 'YYYY-MM-DD'."}, 400

        new_expense = Expense(
            name=data["name"],
            amount=data["amount"],
            date=date,
            user_id=data["user_id"]
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

    def put(self, id):
        data = request.get_json()

        expense = Expense.query.get(id)
        if not expense:
            return {"error": "Expense not found"}, 404

        if "name" in data:
            expense.name = data["name"]
        if "amount" in data:
            expense.amount = data["amount"]
        if "date" in data:
            try:
                expense.date = datetime.strptime(data["date"], "%Y-%m-%d").date()
            except ValueError:
                return {"error": "Invalid date format. Use 'YYYY-MM-DD'."}, 400

        db.session.commit()
        return expense.to_dict(), 200

    def delete(self, id):
        expense = Expense.query.get(id)
        if not expense:
            return {"error": "Expense not found"}, 404

        db.session.delete(expense)
        db.session.commit()
        return {"message": "Expense deleted successfully"}, 200

class CategoryList(Resource):
    def get(self):
        categories = Category.query.all()
        return [category.to_dict() for category in categories], 200

class CategoryDetail(Resource):
    def get(self, id):
        category = Category.query.get(id)
        if not category:
            return {"error": "Category not found"}, 404
        return category.to_dict(), 200

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
    