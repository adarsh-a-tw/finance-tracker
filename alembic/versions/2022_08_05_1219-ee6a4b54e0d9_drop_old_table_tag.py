"""drop old table tag

Revision ID: ee6a4b54e0d9
Revises: 8b86fceb57fa
Create Date: 2022-08-05 12:19:48.968058

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee6a4b54e0d9'
down_revision = '8b86fceb57fa'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("tag")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'tag',
        sa.Column('id', sa.String(50), primary_key=True),
        sa.Column('value', sa.String(70), nullable=False)
    )
    # ### end Alembic commands ###
