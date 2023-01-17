"""add content collumn to posts

Revision ID: aa748b200777
Revises: 85729fe23c5d
Create Date: 2023-01-17 11:21:08.860913

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa748b200777'
down_revision = '85729fe23c5d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
