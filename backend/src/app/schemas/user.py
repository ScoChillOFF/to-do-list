from pydantic import BaseModel


class User(BaseModel):
    id: str
    username: str
    password_hash: str
    

class UserAuth(BaseModel):
    username: str
    password: str
    

class UserResponse(BaseModel):
    id: str
    username: str
    
    @classmethod
    def from_user(cls, user: User) -> "UserResponse":
        return UserResponse(id=user.id, username=user.username)