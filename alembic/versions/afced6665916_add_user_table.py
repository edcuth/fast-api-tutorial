"""add user table

Revision ID: afced6665916
Revises: 65d929ee1b37
Create Date: 2021-11-06 20:19:04.649352

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'afced6665916'
down_revision = '65d929ee1b37'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
    sa.Column(
        'id',
        sa.Integer, 
        nullable=False
    ), sa.Column(
        'email',
        sa.String,
        nullable=False
    ), sa.Column(
        'password',
        sa.String,
        nullable=False
    ), sa.Column(
        'created_at',
        sa.TIMESTAMP(timezone=True),
        server_default=sa.text('now()'),
        nullable=False
    ), sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    pass


def downgrade():
    op.drop_table('users')
    pass
