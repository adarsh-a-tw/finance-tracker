"""alter column_password_length

Revision ID: 14c6562f198a
Revises: 3680376ceaea
Create Date: 2022-08-01 13:42:30.539484

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '14c6562f198a'
down_revision = '3680376ceaea'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('user', 'password',
                    existing_type=sa.String(length=70),
                    type_=sa.String(length=128),
                    nullable=False)


def downgrade() -> None:
    op.alter_column('user', 'password',
                    existing_type=sa.String(length=128),
                    type_=sa.String(length=70),
                    existing_nullable=True)
