from abc import ABC, abstractmethod

from app.schemas.user import User, UserAuth


class UserRepository(ABC):
    @abstractmethod
    def get_user_by_username(username: str) -> User:
        raise NotImplementedError
    
    @abstractmethod
    def add_user(user: UserAuth) -> User:
        raise NotImplementedError
