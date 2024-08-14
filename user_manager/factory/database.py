from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "sqlite+aiosqlite:///db/database.db"

engine = create_async_engine(DATABASE_URL, echo=True)


class SyncSession(Session):
    def get_bind(self, mapper=None, clause=None, **kwargs):
        return engine.sync_engine


SessionLocal = sessionmaker(
    class_=AsyncSession, sync_session_class=SyncSession, expire_on_commit=False
)

Base = declarative_base()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
