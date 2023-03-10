from fastapi import APIRouter
from app.routers.dependencies.userManager import fastapi_users
from app.schemas.user import UserRead, UserUpdate, UserCreate
from app.routers.dependencies.userManager import auth_backend

router = APIRouter()

router.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/jwt", tags=["auth"])
router.include_router(fastapi_users.get_users_router(UserRead, UserUpdate), tags=["users"])
router.include_router(fastapi_users.get_register_router(UserRead, UserCreate), tags=["auth"])
router.include_router(fastapi_users.get_verify_router(UserRead), tags=["auth"])
router.include_router(fastapi_users.get_reset_password_router(), tags=["auth"])
