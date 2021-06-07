from fastapi import APIRouter
from user.routers import authentication, user


user_router = APIRouter()

user_router.include_router(authentication.router)
user_router.include_router(user.router)
