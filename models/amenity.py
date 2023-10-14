#!/usr/bin/python3
"""The Amenity class definition."""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """Represents an amenity.

    Attributes:
        name (str): Name of the amenity.
    """

    name = ""
