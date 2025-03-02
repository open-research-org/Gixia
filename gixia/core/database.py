from dataclasses import asdict
import logging
import os
import pymongo

from gixia.core.user import User


logger = logging.getLogger(__name__)

class Database:
    """
    Data management class for the MongoDB database.
    """
    def __init__(self):
        """
        Initialize the database and downloaders.
        """
        # Initialize database connection and setup collections.
        username = os.environ['MONGO_USERNAME']
        password = os.environ['MONGO_PASSWORD']
        self.client = pymongo.MongoClient(f'mongodb://{username}:{password}@20.2.82.55:27017/')
        db = self.client['gixia']
        self.papers_collection = db['papers']
        self.users_collection = db['users']

    def get_paper(self, arxiv_id):
        """
        Get the paper specified by arXiv ID.
        """
        return self.papers_collection.find_one({'id': arxiv_id})

    def get_user(self, email) -> User:
        """
        Get the user specified by email.

        Args:
            email (str): The email of the user.

        Returns:
            User: The user object specified by email.
        """
        user_document = self.users_collection.find_one({'email': email})
        return User(**user_document) if user_document else None

    def create_user(self, email, name, google_info) -> User:
        """
        Create a new user.

        Args:
            email (str): The email of the user.
            name (str): The name of the user.
            google_info (dict): A dict of Google account info.

        Returns:
            User: The new created user object.
        """
        user = User(email=email, name=name, google_info=google_info)
        self.users_collection.insert_one(asdict(user))
        return user

    def close(self):
        """
        Close the database connection.
        """
        self.client.close()