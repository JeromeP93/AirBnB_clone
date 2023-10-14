#!/usr/bin/python3
"""The City class defination."""
from models.base_model import BaseModel


class City(BaseModel):
    """Represents a city.

    Attributes:
        state_id (str): The state id.
        name (str): Name of the city.
    """

    state_id = ""
    name = ""
