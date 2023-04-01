"""populate move table

Revision ID: 16abe0f4d3ed
Revises: f44fd69cc60a
Create Date: 2023-04-01 18:07:37.478896

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16abe0f4d3ed'
down_revision = 'f44fd69cc60a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    metadata_obj = sa.MetaData()
    metadata_obj.reflect(bind=op.get_bind(), schema = "bjj", only=["move"])
    move_table = sa.Table("move", metadata_obj, schema="bjj")

    op.bulk_insert(move_table,
        [
            {"type": "Submission", "name": "Americana"},
            {"type": "Submission", "name": "Anaconda"},
            {"type": "Takedown", "name": "Ankle Pick"},
            {"type": "Guard Pass", "name": "Arm Behind their Back Guard Pass"},
            {"type": "Takedown", "name": "Arm Drag"},
            {"type": "Submission", "name": "Armbar (Guard)"},
            {"type": "Submission", "name": "Armbar (Mount)"},
            {"type": "Defence", "name": "Armbar Defence (Closed Guard)"},
            {"type": "Defence", "name": "Armbar Defence (Mount)"},
            {"type": "Defence", "name": "Back Control Defence"},
            {"type": "Defence", "name": "Back Control Escape"},
            {"type": "Guard Pass", "name": "Back Take (Generic)"},
            {"type": "Submission", "name": "Baseball Bat Choke"},
            {"type": "Guard Pass", "name": "Berimbolo"},
            {"type": "Submission", "name": "Bow and Arrow Choke"},
            {"type": "Defence", "name": "Bridge and Roll"},
            {"type": "Guard Pass", "name": "Butterfly Guard Pass (Generic)"},
            {"type": "Submission", "name": "Clock Choke"},
            {"type": "Guard Pass", "name": "Closed Guard Break (Generic)"},
            {"type": "Submission", "name": "Cross Choke"},
            {"type": "Defence", "name": "Cross Choke Escape"},
            {"type": "Submission", "name": "D’Arce"},
            {"type": "Guard Pass", "name": "De La Riva Pass (Generic)"},
            {"type": "Sweep", "name": "De La Riva Sweep (Generic)"},
            {"type": "Sweep", "name": "Deep Half Sweep (Generic)"},
            {"type": "Sweep", "name": "Double Ankle Sweep"},
            {"type": "Takedown", "name": "Double Leg"},
            {"type": "Guard Pass", "name": "Double Under Guard Pass"},
            {"type": "Defence", "name": "Embarcada (Reguarding)"},
            {"type": "Defence", "name": "Escape from Mount (Generic)"},
            {"type": "Submission", "name": "Ezekiel"},
            {"type": "Submission", "name": "Gogoplata"},
            {"type": "Takedown", "name": "Guard Pull"},
            {"type": "Defence", "name": "Guard Retention"},
            {"type": "Submission", "name": "Guillotine"},
            {"type": "Defence", "name": "Guillotine Defence (Generic)"},
            {"type": "Guard Pass", "name": "Half Guard Pass (Generic)"},
            {"type": "Sweep", "name": "Half Guard Sweep (Generic)"},
            {"type": "Sweep", "name": "Hip Bump Sweep"},
            {"type": "Sweep", "name": "Idiot Sweep"},
            {"type": "Submission", "name": "Kata Gatame"},
            {"type": "Submission", "name": "Kimura"},
            {"type": "Submission", "name": "Knee Bar"},
            {"type": "Guard Pass", "name": "Knee Cut Pass"},
            {"type": "Defence", "name": "Knee Cut Pass Defence (Generic)"},
            {"type": "Defence", "name": "Knee Elbow Escape"},
            {"type": "Defence", "name": "Knee on Belly Defence (Generic)"},
            {"type": "Takedown", "name": "Kosoto Gari (Small Outside Hook)"},
            {"type": "Submission", "name": "Lapel Choke (Generic)"},
            {"type": "Guard Pass", "name": "Leg Drag Pass"},
            {"type": "Guard Pass", "name": "Logsplitter Guard Pass"},
            {"type": "Submission", "name": "Loop Choke"},
            {"type": "Takedown", "name": "Low Single"},
            {"type": "Submission", "name": "North South Choke"},
            {"type": "Submission", "name": "Omoplata"},
            {"type": "Defence", "name": "Omoplata Escape (Generic)"},
            {"type": "Sweep", "name": "Omoplata Sweep"},
            {"type": "Guard Pass", "name": "Open Guard Passing (Generic)"},
            {"type": "Other", "name": "Other"},
            {"type": "Takedown", "name": "Ouchi Gari (Major Inner Reap)"},
            {"type": "Sweep", "name": "Over Under Butterfly Sweep"},
            {"type": "Sweep", "name": "Pendulum/Flower/Pia Sweep"},
            {"type": "Submission", "name": "Rear Nake Choke"},
            {"type": "Sweep", "name": "Reverse De La Riva Sweep (Generic)"},
            {"type": "Submission", "name": "Reverse Triangle"},
            {"type": "Sweep", "name": "Scissor Sweep"},
            {"type": "Submission", "name": "Seat Belt Choke"},
            {"type": "Takedown", "name": "Seoi Nage"},
            {"type": "Defence", "name": "Side Control Escape (Generic)"},
            {"type": "Guard Pass",
                "name": "Side Control to Full Mount (Generic)"},
            {"type": "Guard Pass",
                "name": "Side Control to Knee on Belly (Generic)"},
            {"type": "Takedown", "name": "Single Leg"},
            {"type": "Takedown", "name": "Single Leg Defence"},
            {"type": "Guard Pass", "name": "Single Leg Stack Pass"},
            {"type": "Defence", "name": "Single Leg X Defence (Generic)"},
            {"type": "Sweep", "name": "Single Leg X Sweep (Generic)"},
            {"type": "Defence", "name": "Sinking"},
            {"type": "Defence", "name": "Sitout"},
            {"type": "Submission", "name": "Sliding Collar Choke"},
            {"type": "Takedown", "name": "Snap Down"},
            {"type": "Guard Pass", "name": "Spider Guard Pass (Generic)"},
            {"type": "Sweep", "name": "Spider Guard Sweep (Generic)"},
            {"type": "Defence", "name": "Sprawl"},
            {"type": "Guard Pass", "name": "Standing Guard Pass"},
            {"type": "Submission", "name": "Straight Ankle Lock"},
            {"type": "Defence", "name": "Straight Ankle Lock Defence"},
            {"type": "Submission", "name": "Straight Armbar"},
            {"type": "Takedown", "name": "Takedown (Generic)"},
            {"type": "Submission", "name": "Toe Hold"},
            {"type": "Guard Pass", "name": "Torreando Pass"},
            {"type": "Submission", "name": "Triangle"},
            {"type": "Defence", "name": "Triangle Escapes"},
            {"type": "Sweep", "name": "Tripod Sweep"},
            {"type": "Defence", "name": "Turtle Defence"},
            {"type": "Guard Pass", "name": "Under Over Pass"},
            {"type": "Sweep", "name": "Underhook Leg on Shoulder Sweep"},
            {"type": "Submission", "name": "Von Flue Choke"},
            {"type": "Submission", "name": "Waka Gatame"},
            {"type": "Submission", "name": "Wrist Lock (Generic)"},
            {"type": "Guard Pass", "name": "X Guard Pass (Generic)"},
            {"type": "Sweep", "name": "X Guard Sweep (Generic)"},
            {"type": "Guard Pass", "name": "X Pass"},
            {"type": "Sweep", "name": "Open Guard Sweep (Generic)"},
            {"type": "Submission", "name": "Heel Hook"},
            {"type": "Submission", "name": "Toe Hold"},
            {"type": "Sweep", "name": "Lasso Sweep (Generic)"},
            {"type": "Pass", "name": "Lasso Pass (Generic)"},
        ]
    )


def downgrade() -> None:
    pass
