from fastapi import FastAPI
from app.routers.users import router as users_router
from app.database import create_db_and_tables

app = FastAPI()

app.include_router(users_router, prefix="/users", tags=["users"])

