from fastapi import FastAPI, Depends, status, Response, HTTPException
from typing import List
from sqlalchemy.orm import Session
from .database import engine, SessionLocal
from . import models
from .schemas import Blog, ShowBlog


app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World Blog"}


@app.get('/blogs', response_model=List[ShowBlog])
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blogs/{id}', status_code=status.HTTP_200_OK, response_model=ShowBlog)
def get_blog_by_id(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).where(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'blog with id {id} was not found')

    return blog


@ app.post('/blogs', status_code=status.HTTP_201_CREATED)
def create_blog(request: Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.put('/blogs/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id: int, request: Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Blog with id {id} not found")
    blog.update(dict(request))
    db.commit()
    return 'updated'


@app.delete('/blogs', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Blog with id {id} not found")

    blog.delete(synchronize_session=False)
    db.commit()
    return 'deleted'

# //////////////////////////////////////////////////////////


@app.post('/user')
def create_user(request: ):
    pass
