"""create post table

Revision ID: e9e9e95ca633
Revises: 
Create Date: 2022-09-13 12:44:07.344259

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9e9e95ca633'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('post',
    sa.Column('id', sa.Integer(), primary_key= True, nullable = False),
    sa.Column('title', sa.String(), nullable = False),
    sa.Column('content', sa.String(), nullable = False),
    sa.Column('published', sa.Boolean(), nullable = False),
    sa.Column('id', sa.Integer(), primary_key= True, nullable = False),
    sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()')),
    sa.Column('owner_id',sa.Integer(),nullable=False)
    )
    
    pass


def downgrade() -> None:
    op.drop_table('post')
    pass
