from uuid import uuid4

import pytest

from app.repositories.exceptions import NotFoundError, ConstraintViolationError
from app.schemas.user import User, UserAuth
from app.services.exceptions import RegistrationError, AuthenticationError
from app.services.users import UserService, UserServiceImpl
from app.repositories.users import UserRepository
from app.services.utils.password_manager import PasswordManager


class UserRepositoryMock(UserRepository):
    users: list[User]

    def __init__(self):
        self.users = [
            User(id="test_id_1", username="JohnDoe", password_hash="johndoehashed"),
            User(id="test_id_2", username="JaneDoe", password_hash="janedoehashed"),
            User(id="test_id_3", username="Bipki", password_hash="bipkihashed")
        ]

    def get_user_by_username(self, username: str) -> User:
        try:
            user = [u for u in self.users if u.username == username].pop()
            return user
        except IndexError:
            raise NotFoundError

    def add_user(self, user: UserAuth) -> User:
        if len([u for u in self.users if u.username == user.username]) > 0:
            raise ConstraintViolationError
        return User(id=str(uuid4()), username=user.username, password_hash=user.password)


class PasswordManagerMock(PasswordManager):
    def is_password_matching_hash(self, raw_password: str, password_hash: str) -> bool:
        return f"{raw_password}hashed" == password_hash

    def generate_password_hash(self, raw_password: str) -> str:
        return f"{raw_password}hashed"


@pytest.fixture
def user_service() -> UserService:
    return UserServiceImpl(UserRepositoryMock(), PasswordManagerMock())


class TestRegisterAndGetUser:
    def test_successful_register(self, user_service):
        user_auth = UserAuth(username="David", password="passw")
        user = user_service.register_and_get_user(user_auth)

        assert all([user.id is not None,
                    user.username == "David",
                    user.password_hash == "passwhashed"])

    def test_not_unique_username(self, user_service):
        user_auth = UserAuth(username="JohnDoe", password="passw")

        with pytest.raises(RegistrationError):
            user_service.register_and_get_user(user_auth)


class TestAuthenticateAndGetUser:
    def test_successful_auth(self, user_service):
        user_auth = UserAuth(username="JohnDoe", password="johndoe")
        user = user_service.authenticate_and_get_user(user_auth)

        assert all([user.id == "test_id_1",
                    user.username == "JohnDoe",
                    user.password_hash == "johndoehashed"])

    def test_invalid_password(self, user_service):
        user_auth = UserAuth(username="JohnDoe", password="wrongpassw")

        with pytest.raises(AuthenticationError):
            user_service.authenticate_and_get_user(user_auth)

    def test_invalid_username(self, user_service):
        user_auth = UserAuth(username="nevermind", password="what")

        with pytest.raises(AuthenticationError):
            user_service.authenticate_and_get_user(user_auth)
