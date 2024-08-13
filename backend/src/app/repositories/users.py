from abc import ABC, abstractmethod

import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from app.schemas.user import User, UserAuth
from .exceptions import NotFoundError, ConstraintViolationError
from .sqlalchemy_db.models.users import UserModel


class UserRepository(ABC):
    @abstractmethod
    def get_user_by_username(self, username: str) -> User:
        """
        Fetches a user from the repository by it`s username; throws an exception if the user does not exist.

        Args:
            username (str): The username of the user to be retrieved.

        Raises:
            NotFoundError: When there is no user with the given username

        Returns:
            User: The user object associated with the specified username.
        """
        pass
    
    @abstractmethod
    def add_user(self, user: UserAuth) -> User:
        """
        This method creates a new user in the repository and throws an exception if the username is not unique.

        Args:
            user (UserAuth): An object representing the user's credentials.

        Raises:
            ConstraintViolationError: If the user's username is not unique.

        Returns:
            User: An object representing the newly created user with a unique ID.
        """
        pass


class UserRepositorySQLAlchemy(UserRepository):
    session_maker: async_sessionmaker[AsyncSession]

    def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
        self.session_maker = session_maker

    async def get_user_by_username(self, username: str) -> User:
        async with self.session_maker() as session:
            query = sa.select(UserModel).where(UserModel.username == username)
            user_model = await session.scalar(query)
            if not user_model:
                raise NotFoundError
            return user_model.to_user()

    async def add_user(self, user: UserAuth) -> User:
        async with self.session_maker() as session:
            user_model = UserModel(username=user.username, password_hash=user.password)
            session.add(user_model)
            try:
                await session.commit()
                await session.refresh(user_model)
                return user_model.to_user()
            except IntegrityError:
                raise ConstraintViolationError
