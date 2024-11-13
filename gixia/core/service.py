from gixia.core.database import Database


class Service():
    def __init__(self):
        """
        Initialize the service.
        """
        self.database = Database()

    def get_paper(self, arxiv_id):
        """
        Get the paper specified by arXiv ID.
        """
        return self.database.get_paper(arxiv_id)

service = Service()