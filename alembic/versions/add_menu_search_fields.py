"""add menu search fields

Revision ID: add_menu_search_fields
Revises: 8b0e0c6d46b4
Create Date: 2024-01-01

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_menu_search_fields'
down_revision = '8b0e0c6d46b4'
branch_labels = None
depends_on = None


def upgrade():
    # Add new columns to menu_items table
    op.add_column('menu_items', sa.Column('dietary_type', sa.String(50), nullable=True))
    op.add_column('menu_items', sa.Column('description', sa.String(500), nullable=True))
    op.add_column('menu_items', sa.Column('tags', sa.String(200), nullable=True))


def downgrade():
    # Remove columns from menu_items table
    op.drop_column('menu_items', 'tags')
    op.drop_column('menu_items', 'description')
    op.drop_column('menu_items', 'dietary_type')
