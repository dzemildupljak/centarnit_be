from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from blog.database import Base, engine
from blog.routers import authentication, blog, user


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(blog.router)
