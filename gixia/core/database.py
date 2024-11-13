import logging
import os
import pymongo


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

    def get_paper(self, arxiv_id):
        """
        Get the paper specified by arXiv ID.
        """
        return self.papers_collection.find_one({'id': arxiv_id})

    def close(self):
        """
        Close the database connection.
        """
        self.client.close()