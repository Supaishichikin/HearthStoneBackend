from fastapi import FastAPI
from app.routers.users import router as users_router
from app.database import create_db_and_tables

app = FastAPI()

app.include_router(users_router, prefix="/users", tags=["users"])

<<<<<<< HEAD
=======

@app.on_event("startup")
async def on_startup():
    # Not needed if you setup a migrations system like Alembic
    await create_db_and_tables()
>>>>>>> 2b0a9588a5ee014709462e5e005018390f7efe24
