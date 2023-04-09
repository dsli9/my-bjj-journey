"""create base tables

Tables created:
    - move
    - position
    - class
    - class_attendance
    - moves_practiced
    - positions_practiced

Revision ID: f44fd69cc60a
Revises: 995c230f8a7b
Create Date: 2023-04-01 16:10:54.062384

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f44fd69cc60a'
down_revision = '995c230f8a7b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "move",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("type", sa.Text, nullable=False),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()")
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()")
        ),
        schema="bjj"

    )

    op.create_table(
        "position",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()")
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()")
        ),
        schema="bjj"
    )

    op.create_table(
        "class",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("type", sa.Text, nullable=False),
        sa.Column("duration", sa.Integer, nullable=False,
                  comment="Duration of class in minutes"),
        sa.Column("location", sa.Text, nullable=False),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()")
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()")
        ),
        schema="bjj"
    )

    op.create_table(
        "class_attendance",
        sa.Column("date", sa.Date, primary_key=True),
        sa.Column(
            "class_id",
            sa.Integer,
            sa.ForeignKey("bjj.class.id"),
            primary_key=True
        ),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()")
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()")
        ),
        schema="bjj"
    )

    op.create_table(
        "moves_practiced",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("date", sa.Date, nullable=False),
        sa.Column(
            "class_id",
            sa.Integer,
            sa.ForeignKey("bjj.class.id"),
            nullable=False
        ),
        sa.Column(
            "move_id", sa.Integer, sa.ForeignKey("bjj.move.id"), nullable=False
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()")
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()")
        ),
        sa.ForeignKeyConstraint(
            ["date", "class_id"],
            ["bjj.class_attendance.date", "bjj.class_attendance.class_id"]
        ),
        schema="bjj"
    )

    op.create_table(
        "positions_practiced",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("date", sa.Date, nullable=False),
        sa.Column(
            "class_id",
            sa.Integer,
            sa.ForeignKey("bjj.class.id"),
            nullable=False
        ),
        sa.Column(
            "position_id",
            sa.Integer,
            sa.ForeignKey("bjj.position.id"),
            nullable=False
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()")
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()")
        ),
        sa.ForeignKeyConstraint(
            ["date", "class_id"],
            ["bjj.class_attendance.date", "bjj.class_attendance.class_id"]
        ),
        schema="bjj"
    )

def downgrade() -> None:
    op.drop_table("moves_practiced", schema="bjj")
    op.drop_table("positions_practiced", schema="bjj")
    op.drop_table("class_attendance", schema="bjj")
    op.drop_table("move", schema="bjj")
    op.drop_table("position", schema="bjj")
    op.drop_table("class", schema="bjj")
