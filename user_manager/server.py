from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from factory.database import SessionLocal, init_db
from api.crud import create_user, get_user, get_users, update_user, delete_user
from user_schema.schemas import UserCreate, UserUpdate, UserResponse

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


# Dependency to get the database session
async def get_db():
    async with SessionLocal() as session:
        yield session


@app.post("/users/", response_model=UserResponse)
async def create_user_view(
    user: UserCreate, db: AsyncSession = Depends(get_db)
):
    return await create_user(db=db, user=user)


@app.get("/users/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/users/", response_model=list[UserResponse])
async def read_users(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    users = await get_users(db, skip=skip, limit=limit)
    return users


@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user_view(
    user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db)
):
    db_user = await update_user(db, user_id, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.delete("/users/{user_id}", response_model=UserResponse)
async def delete_user_view(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await delete_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
