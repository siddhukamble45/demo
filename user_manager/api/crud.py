from db_model.models import User
from user_schema.schemas import UserCreate, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def create_user(db: AsyncSession, user: UserCreate):
    db_user = User(**user.dict())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalar_one_or_none()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


async def update_user(db: AsyncSession, user_id: int, user: UserUpdate):
    result = await db.execute(select(User).filter(User.id == user_id))
    db_user = result.scalar_one_or_none()
    if db_user:
        for key, value in user.dict().items():
            setattr(db_user, key, value)
        await db.commit()
        await db.refresh(db_user)
    return db_user


async def delete_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).filter(User.id == user_id))
    db_user = result.scalar_one_or_none()
    if db_user:
        await db.delete(db_user)
        await db.commit()
    return db_user
