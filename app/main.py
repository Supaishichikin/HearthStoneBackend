from fastapi import FastAPI
from app.routers.users import router as users_router
from app.database import create_db_and_tables

app = FastAPI()

app.include_router(users_router, prefix="/users", tags=["users"])


@app.on_event("startup")
async def on_startup():
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()
