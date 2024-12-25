"""Create tables for users, categories, and expenses

Revision ID: 1a1f3e8f4e24
Revises: 
Create Date: 2024-12-20 13:41:00.641428

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a1f3e8f4e24'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('expenses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_expenses_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('expense_category_association',
    sa.Column('expense_id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], name=op.f('fk_expense_category_association_category_id_categories')),
    sa.ForeignKeyConstraint(['expense_id'], ['expenses.id'], name=op.f('fk_expense_category_association_expense_id_expenses')),
    sa.PrimaryKeyConstraint('expense_id', 'category_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('expense_category_association')
    op.drop_table('expenses')
    op.drop_table('users')
    op.drop_table('categories')
    # ### end Alembic commands ###