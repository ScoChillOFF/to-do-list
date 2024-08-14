from abc import ABC, abstractmethod
from uuid import uuid4

from app.repositories.users import UserRepository
from app.repositories.exceptions import ConstraintViolationError, NotFoundError
from app.schemas.user import User, UserAuth

from .utils.password_manager import PasswordManager
from .exceptions import AuthenticationError, RegistrationError


class UserService(ABC):
    @abstractmethod
    def register_and_get_user(self, user: UserAuth) -> User:
        """
        Registers a user with the given credentials in the repository and returns the user object;
        raises an exception if there are issues with the credentials, such as a non-unique username.

        Args:
            user (UserAuth): An object representing the user's credentials.

        Raises:
            RegistrationError: If there are problems with the credentials (e.g., non-unique username).

        Returns:
            User: The user object with a repository-generated ID and hashed password.
        """
        pass
    
    @abstractmethod
    def authenticate_and_get_user(self, user: UserAuth) -> User:
        """
        Authenticates the user and, if successful, returns the user object. 

        This method checks the provided credentials against the repository. 
        If the credentials are valid, it returns the corresponding user object; 
        otherwise, it raises an exception.

        Args:
            user (UserAuth): An object representing the user's credentials.
            
        Raises:
            AuthenticationError: If the user does not exist or incorrect credentials are provided.

        Returns:
            User: The user object from the repository with matching credentials.
        """
        pass


class UserServiceImpl(UserService):
    user_repo: UserRepository
    password_manager: PasswordManager

    def __init__(self, user_repo: UserRepository, password_manager: PasswordManager):
        self.user_repo = user_repo
        self.password_manager = password_manager

    async def register_and_get_user(self, user: UserAuth) -> User:
        try:
            return await self._try_to_register_and_get_user(user)
        except ConstraintViolationError:
            raise RegistrationError
    
    async def _try_to_register_and_get_user(self, user: UserAuth) -> User:
        user.password = self.password_manager.generate_password_hash(user.password)
        registered_user = await self.user_repo.add_user(user)
        return registered_user

    async def authenticate_and_get_user(self, user: UserAuth) -> User:
        try:
            return await self._try_to_authenticate_and_get_user(user)
        except NotFoundError:
            raise AuthenticationError
    
    async def _try_to_authenticate_and_get_user(self, user: UserAuth) -> User:
        user_from_repo = await self.user_repo.get_user_by_username(user.username)
        if not self.password_manager.is_password_matching_hash(
            user.password, user_from_repo.password_hash
        ):
            raise AuthenticationError
        return user_from_repo


# TODO: Move UserServiceMock to tests after making an API
class UserServiceMock(UserService):
    repo: list[User] = []
    
    def register_and_get_user(self, user: UserAuth) -> User:
        if user.username in [u.username for u in UserServiceMock.repo]:
            raise RegistrationError
        user.password += "hashed"
        reg_user = User(id=str(uuid4()), username=user.username, password_hash=user.password)
        UserServiceMock.repo.append(reg_user)
        return reg_user
    
    def authenticate_and_get_user(self, user: UserAuth) -> User:
        if user.username not in [u.username for u in UserServiceMock.repo]:
            raise AuthenticationError
        user_from_repo = list(filter(lambda u: u.username == user.username, UserServiceMock.repo)).pop()
        if user_from_repo.password_hash != user.password + "hashed":
            raise AuthenticationError
        return user_from_repo
        
