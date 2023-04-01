"""populate position table

Revision ID: 654c8008ac42
Revises: 16abe0f4d3ed
Create Date: 2023-04-01 18:45:33.592040

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '654c8008ac42'
down_revision = '16abe0f4d3ed'
branch_labels = None
depends_on = None


def upgrade() -> None:
    metadata_obj = sa.MetaData()
    metadata_obj.reflect(bind=op.get_bind(), schema = "bjj", only=["position"])
    position_table = sa.Table("position", metadata_obj, schema="bjj")

    op.bulk_insert(position_table,
        [
            {"name": "Back Control"},
            {"name": "Back Mount"},
            {"name": "Butterfly Guard"},
            {"name": "Closed Guard"},
            {"name": "De La Riva Guard"},
            {"name": "Deep Half Guard"},
            {"name": "Full Mount"},
            {"name": "Half Guard"},
            {"name": "Knee on Belly"},
            {"name": "North South"},
            {"name": "Open Guard"},
            {"name": "Other"},
            {"name": "Reverse De La Riva"},
            {"name": "Reverse Half Guard"},
            {"name": "Reverse Kesa Gatame"},
            {"name": "Side Control"},
            {"name": "Single Leg X"},
            {"name": "Spider Guard"},
            {"name": "Stand Up"},
            {"name": "Turtle"},
            {"name": "X Guard"},
            {"name": "Kesa Gatame"},
            {"name": "Kuzure Kesa Gatame"},
            {"name": "Mantis Guard"},
            {"name": "Lasso"},
        ]
    )


def downgrade() -> None:
    pass
