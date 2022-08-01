"""create tag table

Revision ID: 9ac9c09624ae
Revises: f774038ac61f
Create Date: 2022-08-01 12:24:56.290973

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '9ac9c09624ae'
down_revision = 'f774038ac61f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'tag',
        sa.Column('id', sa.String(50), primary_key=True),
        sa.Column('value', sa.String(70), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('tag')
