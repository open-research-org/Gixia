from gixia.core.database import Database
from gixia.core.paper import Paper
from gixia.core.user import User


class Service():
    def __init__(self):
        """
        Initialize the service.
        """
        self.database = Database()

    def get_paper(self, arxiv_id: str) -> Paper | None:
        """
        Get the paper specified by arXiv ID.

        Args:
            arxiv_id (str): The arXiv ID of the paper. Should in format: 'YYMM.XXXXX'.

        Returns:
            Paper: The paper object. None if not found.
        """
        return self.database.get_paper(arxiv_id)

    def login_with_google(self, email: str, name: str, google_info: dict) -> User:
        """
        Log in with Google account.

        Create a new account if the email is not registered.

        Args:
            email (str): The email of the user.
            name (str): The name of the user.
            google_info (dict): A dict of Google account info.
        
        Returns:
            User: The logged in user.
        """
        user = self.database.get_user(email)
        if user is None:
            user = self.database.create_user(email, name, google_info)
        return user


service = Service()