import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession
import sqlalchemy as sa

from app.repositories.exceptions import NotFoundError, ConstraintViolationError
from app.repositories.sqlalchemy_db.models.users import UserModel
from app.repositories.users import UserRepository, UserRepositorySQLAlchemy
from app.repositories.sqlalchemy_db.models.base import Base
from app.schemas.user import User, UserAuth


@pytest.fixture
async def db_engine() -> AsyncEngine:
    db_url = "sqlite+aiosqlite:///test.db"
    engine = create_async_engine(db_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return engine


@pytest.fixture
def session_maker(db_engine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(db_engine, expire_on_commit=False)


@pytest.fixture
async def test_user(session_maker) -> User:
    async with session_maker() as session:
        user_model = UserModel(id="test_id_1",
                               username="JohnDoe",
                               password_hash="johndoehashed")
        session.add(user_model)
        await session.commit()
    return user_model.to_user()


@pytest.fixture
def user_repository(session_maker) -> UserRepository:
    return UserRepositorySQLAlchemy(session_maker)


class TestGetUserByUsername:
    async def test_successful(self, test_user: User, user_repository: UserRepository):
        user = await user_repository.get_user_by_username("JohnDoe")

        assert all([user.id == test_user.id,
                    user.username == test_user.username,
                    user.password_hash == test_user.password_hash])

    async def test_not_existing_username(self, user_repository: UserRepository):
        with pytest.raises(NotFoundError):
            await user_repository.get_user_by_username("notexisting")


class TestAddUser:
    async def test_successful(self, user_repository: UserRepository, session_maker: async_sessionmaker[AsyncSession]):
        user_auth = UserAuth(username="bob", password="bobhashed")
        user = await user_repository.add_user(user_auth)
        async with session_maker() as session:
            query = sa.select(UserModel).where(UserModel.username == user_auth.username)
            user_model = await session.scalar(query)

        assert all([user.password_hash == user_auth.password,
                    user.username == user_auth.username,
                    user.id is not None and user.id == user_model.id,
                    user.username == user_model.username,
                    user.password_hash == user_model.password_hash])

    async def test_duplicate(self, user_repository: UserRepository, test_user: User):
        user_auth = UserAuth(username="JohnDoe", password="beb")

        with pytest.raises(ConstraintViolationError):
            await user_repository.add_user(user_auth)
