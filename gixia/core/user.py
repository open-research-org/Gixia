from dataclasses import dataclass


@dataclass
class User:
    """
    Entity class for User
    """

    email: str
    name: str
    google_info: dict