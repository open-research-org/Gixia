from dataclasses import asdict
import logging
import os
import pymongo

from gixia.core.paper import Paper
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
        ip_address = os.environ['GIXIA_ADDRESS']
        self.client = pymongo.MongoClient(f'mongodb://{username}:{password}@{ip_address}:27017/')
        db = self.client['gixia']
        self.papers_collection = db['papers']
        self.users_collection = db['users']

    def get_paper(self, id: str) -> Paper | None:
        """
        Get the paper specified by ID.
        """
        paper_document = self.papers_collection.find_one({'id': id})
        return Paper.from_document(paper_document) if paper_document else None

    def get_papers(self, ids: list[str]) -> list[Paper]:
        """
        Get the papers specified by IDs. If a paper is not found, it will be ignored.
        """
        paper_documents = self.papers_collection.find({'id': {'$in': ids}})
        return [Paper.from_document(doc) for doc in paper_documents if doc]

    def add_paper(self, paper):
        """
        Add a paper to the database.
        """
        self.papers_collection.insert_one(asdict(paper))

    def update_papers(self, papers: list[Paper]):
        """
        Update a list of papers in the database.
        """
        if not papers:
            return
        operations = [
            pymongo.UpdateOne(
                {'id': paper.id},
                {'$set': asdict(paper)}
            ) for paper in papers
        ]
        self.papers_collection.bulk_write(operations)

    def add_papers(self, papers: list[Paper]):
        """
        Add a list of papers to the database.
        """
        if not papers:
            return
        self.papers_collection.insert_many([asdict(paper) for paper in papers])

    def update_paper(self, paper):
        """
        Update a paper in the database.
        """
        self.papers_collection.update_one({'id': paper.id}, {'$set': asdict(paper)})

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