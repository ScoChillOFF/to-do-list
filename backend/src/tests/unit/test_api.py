from base64 import b64encode
from uuid import uuid4

from fastapi.testclient import TestClient

from app.app import app
from app.dependencies import get_user_service
from app.schemas.user import User, UserAuth
from app.services.exceptions import RegistrationError, AuthenticationError
from app.services.users import UserService


class UserServiceMock(UserService):
    repo: list[User]

    def __init__(self):
        self.repo = [
            User(id="test_id_1", username="JohnDoe", password_hash="johndoehashed"),
            User(id="test_id_2", username="JaneDoe", password_hash="janedoehashed"),
            User(id="test_id_3", username="Bipki", password_hash="bipkihashed")
        ]

    def register_and_get_user(self, user: UserAuth) -> User:
        if user.username in [u.username for u in self.repo]:
            raise RegistrationError
        user.password += "hashed"
        reg_user = User(id=str(uuid4()), username=user.username, password_hash=user.password)
        return reg_user

    def authenticate_and_get_user(self, user: UserAuth) -> User:
        if user.username not in [u.username for u in self.repo]:
            raise AuthenticationError
        user_from_repo = list(filter(lambda u: u.username == user.username, self.repo)).pop()
        if user_from_repo.password_hash != user.password + "hashed":
            raise AuthenticationError
        return user_from_repo


def get_mock_user_service() -> UserService:
    return UserServiceMock()


app.dependency_overrides[get_user_service] = get_mock_user_service
test_client = TestClient(app)


class TestRegister:

    def test_successful_register(self):
        response = test_client.post("/auth/register", json={"username": "bebra", "password": "bebra"})
        assert all([response.status_code == 200,
                    response.json().keys() == {"id", "username"},
                    response.json().get("username") == "bebra"])

    def test_not_unique_username(self):
        response = test_client.post("/auth/register", json={"username": "JohnDoe", "password": "password"})
        assert response.status_code == 422


class TestAuthentication:

    def test_successful_authentication(self):
        encoded_credentials = b64encode(b"JohnDoe:johndoe").decode()
        response = test_client.get("/auth/get-user-info", headers={"Authorization": f"Basic {encoded_credentials}"})
        assert response.status_code == 200

    def test_incorrect_password(self):
        encoded_credentials = b64encode(b"JohnDoe:bebra").decode()
        response = test_client.get("/auth/get-user-info", headers={"Authorization": f"Basic {encoded_credentials}"})
        assert response.status_code == 401

    def test_non_existent_username(self):
        encoded_credentials = b64encode(b"who:bebra").decode()
        response = test_client.get("/auth/get-user-info", headers={"Authorization": f"Basic {encoded_credentials}"})
        assert response.status_code == 401
