from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from backend.config import Config

database_url = Config.get_database_url()
engine = create_async_engine(database_url)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, autoflush=True, expire_on_commit=False)


class Base(DeclarativeBase):
	pass
