from fastapi import FastAPI
from .database import engine
from . import models
from .routers import blog, user


app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(blog.router)
app.include_router(user.router)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @app.get('/blogs', response_model=List[schemas.ShowBlog], tags=["blogs"])
# def get_all_blogs(db: Session = Depends(get_db)):
#     blogs = db.query(models.Blog).all()
#     return blogs


# @app.get('/blogs/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=["blogs"])
# def get_blog_by_id(id: int, response: Response, db: Session = Depends(get_db)):
#     blog = db.query(models.Blog).where(models.Blog.id == id).first()
#     if not blog:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f'blog with id {id} was not found')

#     return blog


# @ app.post('/blogs', status_code=status.HTTP_201_CREATED, tags=["blogs"])
# def create_blog(request: schemas.CreateBlog, db: Session = Depends(get_db)):
#     new_blog = models.Blog(title=request.title,
#                            body=request.body, user_id=request.author)
#     db.add(new_blog)
#     db.commit()
#     db.refresh(new_blog)
#     return new_blog


# @app.put('/blogs/{id}', status_code=status.HTTP_202_ACCEPTED, tags=["blogs"])
# def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
#     blog = db.query(models.Blog).filter(models.Blog.id == id)
#     if not blog.first():
#         return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                              detail=f"Blog with id {id} not found")
#     blog.update(dict(request))
#     db.commit()
#     return 'updated'


# @app.delete('/blogs', status_code=status.HTTP_204_NO_CONTENT, tags=["blogs"])
# def delete_blog(id: int, db: Session = Depends(get_db)):
#     blog = db.query(models.Blog).filter(models.Blog.id == id)
#     if not blog.first():
#         return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                              detail=f"Blog with id {id} not found")

#     blog.delete(synchronize_session=False)
#     db.commit()
#     return 'deleted'

# //////////////////////////////////////////////////////////


# @app.get('/user', response_model=List[schemas.ShowUser], tags=["users"])
# def get_all_users(db: Session = Depends(get_db)):
#     users = db.query(models.User).all()
#     return users


# @app.get('/user/{id}', response_model=schemas.ShowUser, tags=["users"])
# def get_user_by_id(id: int, db: Session = Depends(get_db)):
#     user = db.query(models.User).where(models.User.id == id).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f'user with id {id} was not found')

#     return user


# @app.post('/user', response_model=schemas.ShowUser, tags=["users"])
# def create_user(request: schemas.User, db: Session = Depends(get_db)):
#     new_user = models.User(name=request.name, email=request.email,
#                            username=request.username, password=Hash.bycrpt(request.password))
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user
