#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# Local imports
from app import app
from config import db  # Use the same `db` instance from `config.py`
from models import User, Category, Expense

if __name__ == '__main__':
    fake = Faker()
    print("Starting seed...")

    with app.app_context():
        # Clear existing data (optional, can be used to reset the DB)
        db.session.query(Expense).delete()
        db.session.query(Category).delete()
        db.session.query(User).delete()
        db.session.commit()

        # Seed Users
        users = []
        for _ in range(10):  # Adjust the range for how many users you want to create
            user = User(
                username=fake.user_name(),
                email=fake.email(),
                password=fake.password()
            )
            db.session.add(user)
            users.append(user)  # Add user to the list for later reference
        db.session.commit()
        print(f"Seeded {len(users)} users.")

        # Seed Categories
        categories = [
            "Food", "Rent", "Travel", "Entertainment", "Utilities",
            "Healthcare", "Education", "Miscellaneous"
        ]
        category_objects = []
        for category in categories:
            category_obj = Category(name=category)
            db.session.add(category_obj)
            category_objects.append(category_obj)  # Add category to the list
        db.session.commit()
        print(f"Seeded {len(category_objects)} categories.")

        # Seed Expenses
        expenses = []
        for _ in range(50):  # Adjust the range for how many expenses you want to create
            expense = Expense(
                name=fake.sentence(),
                amount=round(randint(5, 500) * 0.5, 2),  # Random amounts between $5 and $500
                date=fake.date_this_year(),
                category_id=rc(category_objects).id,  # Assign valid category_id
                user_id=rc(users).id  # Assign valid user_id
            )
            expenses.append(expense)
        db.session.bulk_save_objects(expenses)
        db.session.commit()
        print(f"Seeded {len(expenses)} expenses.")

    print("Seeding complete.")
    