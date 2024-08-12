from uuid import uuid4

import sqlalchemy.orm as so

from .base import Base
from app.schemas.user import User


class UserModel(Base):
    __tablename__ = "users"

    id: so.Mapped[str] = so.mapped_column(primary_key=True, default=lambda: str(uuid4()))
    username: so.Mapped[str] = so.mapped_column(unique=True, index=True)
    password_hash: so.Mapped[str]

    def to_user(self) -> User:
        return User(id=self.id,
                    username=self.username,
                    password_hash=self.password_hash)
