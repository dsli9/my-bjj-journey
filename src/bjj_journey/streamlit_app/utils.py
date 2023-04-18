"""bjj_journey.streamlit_app.utils - Utilities for the BJJ dashboard app.

"""
from typing import List
import streamlit as st


VALID_SKILL_TYPES = {"position", "move"}


def add_vertical_space(num_breaks: int):
    """Add a non-breaking space to create vertical space between elements.

    The number of spaces added depends on the input.
    """
    for _ in range(num_breaks):
        st.write("&nbsp;")


def validate_skill_type(skill_type: str) -> None:
    """
    Validate that the passed-in skill type is on the following: position, move.
    """
    assert (
        skill_type in VALID_SKILL_TYPES
    ), f"Expected one of {VALID_SKILL_TYPES}, got {skill_type} instead"


def resolve_most_practiced_headline(
    dashboard_view: str, skills: List[str], skill_type: str
) -> str:
    """Resolve the headline for the most practiced skill based on the inputs."""
    validate_skill_type(skill_type)

    verb = "was"
    if len(skills) > 1:
        verb = "were"
        skill_type += "s"

    if dashboard_view == "Overall":
        return f"{skills} {verb} the most practiced {skill_type} overall"

    return f"{skills} {verb} the most practiced {skill_type} in {dashboard_view}"
