from fastapi import APIRouter
from .endpoints.admin_auth import admin_auth_router
from .endpoints.admin_movie_crud import admin_movie_router
from .endpoints.user_auth import user_auth_router
from .endpoints.admin_room_crud import admin_room_router
from .endpoints.users import users_router

router = APIRouter()

router.include_router(admin_auth_router)
router.include_router(admin_movie_router)
router.include_router(user_auth_router)
router.include_router(admin_room_router)
router.include_router(users_router)
