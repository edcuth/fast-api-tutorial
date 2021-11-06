"""add content column to post table

Revision ID: 65d929ee1b37
Revises: c3d4e237e529
Create Date: 2021-11-06 20:13:24.101438

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65d929ee1b37'
down_revision = 'c3d4e237e529'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'posts',
        sa.Column(
            'content',
            sa.String,
            nullable=False
        ))
    pass


def downgrade():
    op.drop_column(
        'posts',
        'content'
    )
    pass
