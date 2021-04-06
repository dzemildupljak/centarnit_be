from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from blog import models, schemas


def get_all_blogs(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs


def get_blog_by_id(id: int, db: Session):
    blog = db.query(models.Blog).where(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'blog with id {id} was not found')

    return blog


def create_blog(blog: schemas.CreateBlog, db: Session):
    new_blog = models.Blog(title=blog.title,
                           body=blog.body, user_id=blog.author)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def update_blog(id: int, blog_req: schemas.Blog, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Blog with id {id} not found")
    blog.update(dict(blog_req))
    db.commit()
    return 'updated'


def delete_blog(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Blog with id {id} not found")

    blog.delete(synchronize_session=False)
    db.commit()
    return 'deleted'