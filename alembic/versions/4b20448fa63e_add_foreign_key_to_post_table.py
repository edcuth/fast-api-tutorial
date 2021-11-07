"""add foreign-key to post table

Revision ID: 4b20448fa63e
Revises: afced6665916
Create Date: 2021-11-07 11:41:33.565159

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b20448fa63e'
down_revision = 'afced6665916'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',
    sa.Column(
        'owner_id',
        sa.Integer,
        nullable=False
    ))
    op.create_foreign_key( # to add FKs
        'post_user_fk', #arbitrary name
        source_table="posts", # Table with the foreign key, the many of a one to many relationship
        referent_table="users", # Original table of the key, the one in a one to many relationship
        local_cols=['owner_id'], # Column of the many-side table
        remote_cols=['id'], # column of the one-side table
        ondelete="CASCADE" # on delete action
    )
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
