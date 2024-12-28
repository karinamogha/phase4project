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
    # Debug: Print the database URI and test the connection
    # print("Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])
    
    # with app.app_context():
    #     try:
    #         db.engine.connect()
    #         print("Database connection successful.")
    #     except Exception as e:
    #         print("Error connecting to database:", e)
    #         exit(1)  # Exit early if the database connection fails

        fake = Faker()
        print("Starting seed...")

        # Clear existing data (optional, can be used to reset the DB)
        db.session.query(Expense).delete()
        db.session.query(Category).delete()
        db.session.query(User).delete()

        # Commit the deletions (if resetting the DB)
        db.session.commit()

        # Seed Users
        users = []
        for _ in range(10):  # Adjust the range for how many users you want to create
            user = User(
                username=fake.user_name(),
                email=fake.email(),  # Added email field
                password=fake.password()
            )
            users.append(user)
        db.session.bulk_save_objects(users)
        db.session.commit()
        print(f"Seeded {len(users)} users.")

        # Seed Categories
        categories = [
            "Food", "Rent", "Travel", "Entertainment", "Utilities",
            "Healthcare", "Education", "Miscellaneous"
        ]
        category_objects = [Category(name=category) for category in categories]
        db.session.bulk_save_objects(category_objects)
        db.session.commit()
        print(f"Seeded {len(categories)} categories.")

        # Seed Expenses
        expenses = []
        for _ in range(50):  # Adjust the range for how many expenses you want to create
            expense = Expense(
                name=fake.sentence(),
                amount=round(randint(5, 500) * 0.5, 2),  # Random amounts between $5 and $500
                date=fake.date_this_year(),
                category_id=rc(category_objects).id,
                user_id=rc(users).id
            )
            expenses.append(expense)
        db.session.bulk_save_objects(expenses)
        db.session.commit()
        print(f"Seeded {len(expenses)} expenses.")

        print("Seeding complete.")
        