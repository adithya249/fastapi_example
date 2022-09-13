"""add foreign key to post table

Revision ID: 63a94c8faf57
Revises: 6146bfa63718
Create Date: 2022-09-13 14:38:55.792800

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63a94c8faf57'
down_revision = '6146bfa63718'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_foreign_key('post_users_fk', source_table="post", referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="post")
    op.drop_column('post', 'owner_id')
    pass
