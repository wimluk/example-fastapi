"""add foreign-key to posts

Revision ID: a62d717af685
Revises: 8d69a6cf6f25
Create Date: 2023-01-17 13:03:43.491637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a62d717af685'
down_revision = '8d69a6cf6f25'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts'), 
    op.drop_column('posts', 'owner_id')
    pass
