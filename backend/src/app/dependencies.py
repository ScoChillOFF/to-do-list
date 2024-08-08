from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasicCredentials, HTTPBasic

from app.schemas.user import UserAuth, User
from app.services.exceptions import AuthenticationError
from app.services.users import UserServiceMock, UserService


def get_user_service() -> UserService:
    return UserServiceMock()


def get_user_auth(credentials: Annotated[HTTPBasicCredentials, Depends(HTTPBasic())]) -> UserAuth:
    return UserAuth(username=credentials.username, password=credentials.password)


def get_user(user_auth: Annotated[UserAuth, Depends(get_user_auth)],
             user_service: Annotated[UserService, Depends(get_user_service)]) -> User:
    try:
        user = user_service.authenticate_and_get_user(user_auth)
        return user
    except AuthenticationError:
        raise HTTPException(401)
