"""create association tables

Revision ID: 3680376ceaea
Revises: 9ac9c09624ae
Create Date: 2022-08-01 12:26:29.674068

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '3680376ceaea'
down_revision = '9ac9c09624ae'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'record_tag_mapping',
        sa.Column("record_id", sa.String(50), sa.ForeignKey("record.id"), primary_key=True),
        sa.Column("tag_id", sa.String(50), sa.ForeignKey("tag.id"), primary_key=True),
    )
    op.create_table(
        'record_book_tag_mapping',
        sa.Column("record_book_id", sa.String(50), sa.ForeignKey("record_book.id"), primary_key=True),
        sa.Column("tag_id", sa.String(50), sa.ForeignKey("tag.id"), primary_key=True),
    )


def downgrade() -> None:
    op.drop_table('record_tag_mapping')
    op.drop_table('record_book_tag_mapping')
