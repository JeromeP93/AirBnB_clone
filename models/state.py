#!/usr/bin/python3
"""The State class defination."""
from models.base_model import BaseModel


class State(BaseModel):
    """Represents a state.

    Attributes:
        name (str): The name of a state.
    """

    name = ""
