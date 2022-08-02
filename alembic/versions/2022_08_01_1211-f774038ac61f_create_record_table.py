"""create record_table

Revision ID: f774038ac61f
Revises: ef38953e34b6
Create Date: 2022-08-01 12:11:58.921086

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
from sqlalchemy import ForeignKey

from src.model.record_type import RecordType

revision = 'f774038ac61f'
down_revision = 'ef38953e34b6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'record',
        sa.Column('id', sa.String(50), primary_key=True),
        sa.Column('note', sa.Text(), nullable=False),
        sa.Column('record_book_id', sa.String(70), ForeignKey('record_book.id'), nullable=False),
        sa.Column('amount', sa.Float(), default=0),
        sa.Column('type', sa.String(10), default=RecordType.EXPENSE),
        sa.Column('added_at', sa.DateTime())
    )


def downgrade() -> None:
    op.drop_table('record')
