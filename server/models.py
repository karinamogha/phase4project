from sqlalchemy import CheckConstraint
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from config import db  # Import the single `db` instance from `config.py`

class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)  # Added email field
    password = db.Column(db.String, nullable=False)

    expenses = db.relationship(
        "Expense", back_populates="user", cascade="all, delete-orphan"
    )

    # Exclude password and expenses from serialization
    serialize_rules = ("-password", "-expenses.user")

    # Add a constraint to limit the username length to 50 characters
    __table_args__ = (
        CheckConstraint("LENGTH(username) <= 50", name="username_length_check"),
    )

    def __repr__(self):
        return f"<User {self.username}, {self.email}>"

    @validates("email")
    def validate_email(self, key, value):
        if "@" not in value or "." not in value:
            raise ValueError("Invalid email format")
        return value

    @validates("username")
    def validate_username(self, key, value):
        if len(value) > 50:
            raise ValueError("Username must be 50 characters or fewer")
        return value


class Category(db.Model, SerializerMixin):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    expenses = db.relationship("Expense", back_populates="category")

    # Exclude related expenses from serialization
    serialize_rules = ("-expenses.category",)

    def __repr__(self):
        return f"<Category {self.name}>"


class Expense(db.Model, SerializerMixin):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)

    user = db.relationship("User", back_populates="expenses")
    category = db.relationship("Category", back_populates="expenses")

    # Exclude user and category details from serialized output
    serialize_rules = ("-user.expenses", "-category.expenses")

    @validates("amount")
    def validate_amount(self, key, value):
        if value <= 0:
            raise ValueError("Amount must be greater than 0.")
        return value

    @validates("date")
    def validate_date(self, key, value):
        if not value:
            raise ValueError("Date is required.")
        return value

    def __repr__(self):
        return f"<Expense {self.name}, ${self.amount}, {self.date}>"
    