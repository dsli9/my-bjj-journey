"""create bjj schema

Revision ID: 995c230f8a7b
Revises:
Create Date: 2023-04-01 15:34:12.851872

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '995c230f8a7b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA bjj")


def downgrade() -> None:
    op.execute("DROP SCHEMA bjj")
