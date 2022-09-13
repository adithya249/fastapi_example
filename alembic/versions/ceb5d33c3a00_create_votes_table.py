"""create votes table

Revision ID: ceb5d33c3a00
Revises: 63a94c8faf57
Create Date: 2022-09-13 14:53:40.942878

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ceb5d33c3a00'
down_revision = '63a94c8faf57'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('votes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    pass


def downgrade() -> None:
    op.drop_table('votes')
    pass
