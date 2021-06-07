from fastapi import APIRouter
from blog.routers import blog


blog_router = APIRouter()

blog_router.include_router(blog.router)
