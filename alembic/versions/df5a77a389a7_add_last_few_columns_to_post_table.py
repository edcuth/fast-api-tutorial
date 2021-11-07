"""add last few columns to post table

Revision ID: df5a77a389a7
Revises: 4b20448fa63e
Create Date: 2021-11-07 11:48:08.767020

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df5a77a389a7'
down_revision = '4b20448fa63e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',
    sa.Column(
        'published',
        sa.Boolean,
        nullable=False,
        server_default='TRUE'
    ))
    op.add_column('posts',
    sa.Column(
        'created_at',
        sa.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=sa.text('NOW()')
    ))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
