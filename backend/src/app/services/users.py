from abc import ABC, abstractmethod
from app.repositories.users import UserRepository
from app.schemas.user import User, UserAuth
from .utils.password_manager import PasswordManager


class UserService(ABC):
    @abstractmethod
    def register_user(user: UserAuth) -> User:
        raise NotImplementedError
    
    @abstractmethod
    def authentificate_and_get_user(user: UserAuth) -> User | None:
        raise NotImplementedError


class UserServiceImpl(UserService):
    user_repo: UserRepository
    password_manager: PasswordManager

    def __init__(self, user_repo: UserRepository, password_manager: PasswordManager):
        self.user_repo = user_repo
        self.password_manager = password_manager

    def register_user(self, user: UserAuth) -> User:
        user.password = self.password_manager.generate_password_hash(user.password)
        return self.user_repo.add_user(user)

    def authentificate_and_get_user(self, user: UserAuth) -> User | None:
        user_from_repo = self.user_repo.get_user_by_username(user.username)
        if not user_from_repo:
            return None
        if not self.password_manager.is_password_matching_hash(
            user.password, user_from_repo.password_hash
        ):
            return None
        return user_from_repo
