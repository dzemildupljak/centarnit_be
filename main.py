from sqlalchemy import engine
from database import Base
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from blog.main import blog_router
from user.main import user_router

app = FastAPI()

Base.metadata.create_all(engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router)
app.include_router(blog_router)


@app.get("/")
async def root():
    return {"message": "Hello World Main"}
