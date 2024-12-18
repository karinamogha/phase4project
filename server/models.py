from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

# Configure metadata
metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    expenses = db.relationship(
        "Expense", back_populates="user", cascade="all, delete-orphan"
    )

    serialize_rules = ("-expenses.user",)

    def __repr__(self):
        return f"<User {self.username}>"


class Category(db.Model, SerializerMixin):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    expenses = db.relationship("Expense", back_populates="category")

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

    serialize_rules = ("-user.expenses", "-category.expenses",)

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