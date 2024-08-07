from abc import ABC, abstractmethod

from app.schemas.user import User, UserAuth


class UserRepository(ABC):
    @abstractmethod
    def get_user_by_username(username: str) -> User:
        """
        Fetches a user from the repository by it`s username; throws an exception if the user does not exist.

        Args:
            username (str): The username of the user to be retrieved.

        Raises:
            NotFoundError: When there is no user with the given username
            RepositoryConnectionError: When repository cannot be accessed

        Returns:
            User: The user object associated with the specified username.
        """
        pass
    
    @abstractmethod
    def add_user(user: UserAuth) -> User:
        """
        This method creates a new user in the repository and throws an exception if the username is not unique.

        Args:
            user (UserAuth): An object representing the user's credentials.

        Raises:
            ConstraintViolationError: If the user's username is not unique.
            RepositoryConnectionError: If the repository cannot be accessed.

        Returns:
            User: An object representing the newly created user with a unique ID.
        """
        pass
