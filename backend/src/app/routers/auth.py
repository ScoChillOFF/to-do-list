from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_user_service, get_user
from app.schemas.user import UserAuth, UserResponse, User
from app.services.exceptions import RegistrationError
from app.services.users import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register_user(user_to_register: UserAuth,
                        user_service: Annotated[UserService, Depends(get_user_service)]) -> UserResponse:
    try:
        registered_user = await user_service.register_and_get_user(user_to_register)
        return UserResponse.from_user(registered_user)
    except RegistrationError:
        raise HTTPException(422, detail="Username already taken")


@router.get("/get-user-info")
async def get_user_info(user: Annotated[User, Depends(get_user)]) -> UserResponse:
    return UserResponse.from_user(user)
