"""populate class table

Revision ID: a3e0e80c6dfa
Revises: 654c8008ac42
Create Date: 2023-04-01 18:45:41.179912

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a3e0e80c6dfa"
down_revision = "654c8008ac42"
branch_labels = None
depends_on = None


def upgrade() -> None:
    metadata_obj = sa.MetaData()
    metadata_obj.reflect(bind=op.get_bind(), schema = "bjj", only=["class"])
    class_table = sa.Table("class", metadata_obj, schema="bjj")

    op.bulk_insert(class_table,
        [
            {"type": "Gi", "duration": 75,
                "location": "Gentle Art Studio Astoria",
                "name": "Monday 10:00 AM BJJ Techniques"},
            {"type": "Gi", "duration": 75,
                "location": "Gentle Art Studio Astoria",
                "name": "Monday 6:15 PM BJJ Techniques"},
            {"type": "Gi", "duration": 60,
                "location": "Gentle Art Studio Astoria",
                "name": "Monday 7:30PM Open Mat"},
            {"type": "Gi", "duration": 75,
                "location": "Gentle Art Studio Astoria",
                "name": "Tuesday 6:00 AM BJJ Techniques"},
            {"type": "Gi", "duration": 75,
                "location": "Gentle Art Studio Astoria",
                "name": "Tuesday 10:00 AM BJJ Techniques"},
            {"type": "No Gi", "duration": 60,
                "location": "Gentle Art Studio Astoria",
                "name": "Tuesday 11:30 AM No Gi Techniques"},
            {"type": "Gi", "duration": 75,
                "location": "Gentle Art Studio Astoria",
                "name": "Tuesday 6:15 PM BJJ Techniques"},
            {"type": "Gi", "duration": 60,
                "location": "Gentle Art Studio Astoria",
                "name": "Tuesday 6:15 PM BJJ Focus"},
            {"type": "No Gi", "duration": 60,
                "location": "Gentle Art Studio Astoria",
                "name": "Tuesday 7:30 PM No Gi Advanced"},
            {"type": "Gi", "duration": 75,
                "location": "Gentle Art Studio Astoria",
                "name": "Wednesday 10:00 AM BJJ Techniques"},
            {"type": "Gi", "duration": 75,
                "location": "Gentle Art Studio Astoria",
                "name": "Wednesday 6:15 PM BJJ Techniques"},
            {"type": "No Gi", "duration": 60,
                "location": "Gentle Art Studio Astoria",
                "name": "Wednesday 7:30 PM No Gi Techniques"},
            {"type": "Gi", "duration": 75,
                "location": "Gentle Art Studio Astoria",
                "name": "Thursday 6:00 AM BJJ Techniques"},
            {"type": "Gi", "duration": 75,
                "location": "Gentle Art Studio Astoria",
                "name": "Thursday 10:00 AM BJJ Techniques"},
            {"type": "No Gi", "duration": 60,
                "location": "Gentle Art Studio Astoria",
                "name": "Thursday 11:30 AM No Gi Techniques"},
            {"type": "Gi", "duration": 75,
                "location": "Gentle Art Studio Astoria",
                "name": "Thursday 6:15 PM BJJ Techniques"},
            {"type": "Gi", "duration": 60,
                "location": "Gentle Art Studio Astoria",
                "name": "Thursday 6:15 PM BJJ Focus"},
            {"type": "No Gi", "duration": 60,
                "location": "Gentle Art Studio Astoria",
                "name": "Thursday 7:30 PM No Gi Advanced"},
            {"type": "Gi", "duration": 75,
                "location": "Gentle Art Studio Astoria",
                "name": "Friday 10:00 AM BJJ Techniques"},
            {"type": "Gi", "duration": 75,
                "location": "Gentle Art Studio Astoria",
                "name": "Friday 6:15 PM BJJ Techniques"},
            {"type": "No Gi", "duration": 60,
                "location": "Gentle Art Studio Astoria",
                "name": "Friday 7:30 PM No Gi Techniques"},
            {"type": "No Gi", "duration": 60,
                "location": "Gentle Art Studio Astoria",
                "name": "Saturday 11:00 AM No Gi Techniques"},
            {"type": "Gi", "duration": 75,
                "location": "Gentle Art Studio Astoria",
                "name": "Saturday 12:00 PM BJJ Lab"},
            {"type": "Gi", "duration": 60,
                "location": "Gentle Art Studio Astoria",
                "name": "Saturday 1:15 PM Open Mat"},
            {"type": "Gi", "duration": 60,
                "location": "Gentle Art Studio Astoria",
                "name": "Sunday 10:00 AM Open Mat"},
        ]
    )


def downgrade() -> None:
    pass
