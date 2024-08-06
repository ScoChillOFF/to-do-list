from pydantic import BaseModel


class User(BaseModel):
    id: str
    username: str
    password_hash: str
    

class UserAuth(BaseModel):
    username: str
    password: str