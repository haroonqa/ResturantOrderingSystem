"""Update promotion table

Revision ID: 235943d8a130
Revises: 
Create Date: 2024-12-03 18:51:06.264732

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '235943d8a130'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_staff_id', table_name='staff')
    op.drop_index('username', table_name='staff')
    op.drop_table('staff')
    op.drop_index('ix_transactions_id', table_name='transactions')
    op.drop_table('transactions')
    op.add_column('orders', sa.Column('order_completed', sa.Boolean(), nullable=True))
    op.add_column('orders', sa.Column('customer_id', sa.Integer(), nullable=True))
    op.add_column('orders', sa.Column('promotion_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'orders', 'customers', ['customer_id'], ['id'])
    op.create_foreign_key(None, 'orders', 'promotion', ['promotion_id'], ['id'])
    op.drop_column('orders', 'description')
    op.drop_column('orders', 'customer_name')
    op.add_column('recipes', sa.Column('resources_needed', sa.JSON(), nullable=True))
    op.drop_index('ix_recipes_amount', table_name='recipes')
    op.drop_constraint('recipes_ibfk_2', 'recipes', type_='foreignkey')
    op.drop_column('recipes', 'amount')
    op.drop_column('recipes', 'resource_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recipes', sa.Column('resource_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('recipes', sa.Column('amount', mysql.INTEGER(), server_default=sa.text("'0'"), autoincrement=False, nullable=False))
    op.create_foreign_key('recipes_ibfk_2', 'recipes', 'resources', ['resource_id'], ['id'])
    op.create_index('ix_recipes_amount', 'recipes', ['amount'], unique=False)
    op.drop_column('recipes', 'resources_needed')
    op.add_column('orders', sa.Column('customer_name', mysql.VARCHAR(length=100), nullable=True))
    op.add_column('orders', sa.Column('description', mysql.VARCHAR(length=300), nullable=True))
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.drop_column('orders', 'promotion_id')
    op.drop_column('orders', 'customer_id')
    op.drop_column('orders', 'order_completed')
    op.create_table('transactions',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('order_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('price', mysql.DECIMAL(precision=4, scale=2), server_default=sa.text("'0.00'"), nullable=False),
    sa.Column('payment_method', mysql.VARCHAR(length=4), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], name='transactions_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_transactions_id', 'transactions', ['id'], unique=False)
    op.create_table('staff',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', mysql.VARCHAR(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('username', 'staff', ['username'], unique=True)
    op.create_index('ix_staff_id', 'staff', ['id'], unique=False)
    # ### end Alembic commands ###
