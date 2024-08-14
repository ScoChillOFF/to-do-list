from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasicCredentials, HTTPBasic

from app.repositories.sqlalchemy_db.engine import engine
from app.repositories.users import UserRepositorySQLAlchemy
from app.schemas.user import UserAuth, User
from app.services.exceptions import AuthenticationError
from app.services.users import UserServiceImpl, UserService
from app.services.utils.password_manager import PasswordManagerBcrypt


def get_user_service() -> UserService:
    return UserServiceImpl(UserRepositorySQLAlchemy(engine), PasswordManagerBcrypt())


def get_user_auth(credentials: Annotated[HTTPBasicCredentials, Depends(HTTPBasic())]) -> UserAuth:
    return UserAuth(username=credentials.username, password=credentials.password)


async def get_user(user_auth: Annotated[UserAuth, Depends(get_user_auth)],
                   user_service: Annotated[UserService, Depends(get_user_service)]) -> User:
    try:
        user = await user_service.authenticate_and_get_user(user_auth)
        return user
    except AuthenticationError:
        raise HTTPException(401)
