#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# Local imports
from server.config import app, db
from server.models import User, Category, Expense

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting seed...")

        # Clear existing data
        db.session.query(Expense).delete()
        db.session.query(Category).delete()
        db.session.query(User).delete()
        db.session.commit()

        # Seed Users
        users = []
        for _ in range(10):  # Adjust the range for user count
            user = User(
                username=fake.user_name(),
                password=fake.password()
            )
            users.append(user)
        db.session.bulk_save_objects(users)
        db.session.commit()
        print(f"Seeded {len(users)} users.")

        # Fetch all user IDs after committing
        user_ids = [user.id for user in User.query.all()]

        # Seed Categories
        categories = [
            "Food", "Rent", "Travel", "Entertainment", "Utilities", "Healthcare", "Education", "Miscellaneous"
        ]
        category_objects = [Category(name=category) for category in categories]
        db.session.bulk_save_objects(category_objects)
        db.session.commit()
        print(f"Seeded {len(categories)} categories.")

        # Fetch all category IDs after committing
        category_ids = [category.id for category in Category.query.all()]

        # Seed Expenses
        for _ in range(50):  # Adjust the range for expense count
            expense = Expense(
                name=fake.sentence(),
                amount=round(randint(5, 500) * 0.5, 2),
                date=fake.date_this_year(),
                user_id=rc(user_ids),  # Assign random user_id
            )
            db.session.add(expense)  # Add expense to the session
            expense.categories.append(db.session.get(Category, rc(category_ids)))  # Assign random category
        db.session.commit()
        print(f"Seeded 50 expenses.")

        print("Seeding complete.")