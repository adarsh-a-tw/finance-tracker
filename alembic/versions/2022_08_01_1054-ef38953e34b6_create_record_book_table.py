"""create record_book_table

Revision ID: ef38953e34b6
Revises: 0d330c97f346
Create Date: 2022-08-01 10:54:42.560955

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
from sqlalchemy import ForeignKey

revision = 'ef38953e34b6'
down_revision = '0d330c97f346'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'record_book',
        sa.Column('id', sa.String(50), primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('user_id', sa.String(70), ForeignKey('user.id'), nullable=False),
        sa.Column('net_balance', sa.Float(), default=0),
    )


def downgrade() -> None:
    op.drop_table('record_book')
