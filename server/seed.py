#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, User, Category, Expense

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
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
                email=fake.email(),
                password=fake.password()
            )
            users.append(user)
        db.session.bulk_save_objects(users)
        db.session.commit()
        print(f"Seeded {len(users)} users.")

        # Seed Categories
        categories = [
            "Food", "Rent", "Travel", "Entertainment", "Utilities", "Healthcare", "Education", "Miscellaneous"
        ]
        category_objects = [Category(name=category) for category in categories]
        db.session.bulk_save_objects(category_objects)
        db.session.commit()
        print(f"Seeded {len(categories)} categories.")

        # Seed Expenses
        expenses = []
        for _ in range(50):  # Adjust the range for how many expenses you want to create
            expense = Expense(
                description=fake.sentence(),
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

