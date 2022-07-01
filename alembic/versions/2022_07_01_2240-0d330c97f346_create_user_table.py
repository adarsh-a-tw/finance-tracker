"""create user table

Revision ID: 0d330c97f346
Revises: 
Create Date: 2022-07-01 22:40:45.653452

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0d330c97f346'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'user',
        sa.Column('id', sa.String(50), primary_key=True),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('email', sa.String(70), nullable=False),
        sa.Column('password', sa.String(70)),
        sa.Column('salt', sa.String(70)),
    )


def downgrade() -> None:
    op.drop_table('user')
