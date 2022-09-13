"""create user table

Revision ID: 6146bfa63718
Revises: e9e9e95ca633
Create Date: 2022-09-13 14:29:35.462786

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6146bfa63718'
down_revision = 'e9e9e95ca633'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    
                    sa.UniqueConstraint('email')
    )
    
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
