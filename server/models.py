from server.config import db
from sqlalchemy import CheckConstraint, Table
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

# Association Table
expense_category_association = Table(
    "expense_category_association",
    db.Model.metadata,
    db.Column("expense_id", db.Integer, db.ForeignKey("expenses.id"), primary_key=True),
    db.Column("category_id", db.Integer, db.ForeignKey("categories.id"), primary_key=True),
)

class User(db.Model, SerializerMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    expenses = db.relationship("Expense", back_populates="user", cascade="all, delete-orphan")

    serialize_rules = ("-expenses.user",)

    def __repr__(self):
        return f"<User {self.username}>"

class Category(db.Model, SerializerMixin):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    expenses = db.relationship(
        "Expense", secondary=expense_category_association, back_populates="categories"
    )

    serialize_rules = ("-expenses.categories",)

    def __repr__(self):
        return f"<Category {self.name}>"

class Expense(db.Model, SerializerMixin):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", back_populates="expenses")
    categories = db.relationship(
        "Category", secondary=expense_category_association, back_populates="expenses"
    )

    serialize_rules = ("-user.expenses", "-categories.expenses")

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