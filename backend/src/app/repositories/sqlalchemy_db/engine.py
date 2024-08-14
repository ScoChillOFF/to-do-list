import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import sqlalchemy as sa

from app.config import config


engine = create_async_engine(config.sqlalchemy_db_url)


async def check_conn() -> None:
    async with AsyncSession(engine) as session:
        await session.execute(sa.text("SELECT 1"))
        print("CONN SUCCESSFUL")


if __name__ == "__main__":
    asyncio.run(check_conn())
