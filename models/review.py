#!/usr/bin/python3
"""The Review class defination."""
from models.base_model import BaseModel


class Review(BaseModel):
    """Represents a review.

    Attributes:
        place_id (str): The Place id.
        user_id (str): The User id.
        text (str): The review texts.
    """

    place_id = ""
    user_id = ""
    text = ""
