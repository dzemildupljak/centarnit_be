import os
from fastapi import HTTPException, status, UploadFile, File
import shutil
from sqlalchemy.orm import Session
from blog import models, schemas


def get_all_blogs(db: Session):
    blogs = db.query(models.blog.Blog).all()
    return blogs


def get_all_blogs_by_author(user_id: int, db: Session):
    blogs = db.query(models.blog.Blog).filter(
        models.blog.Blog.user_id == user_id).all()
    return blogs


def get_blog_by_id(id: int, db: Session):
    blog = db.query(models.blog.Blog).where(models.blog.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'blog with id {id} was not found')

    return blog


def get_my_blog_by_id(id: int, author_id: int, db: Session):
    blog = db.query(models.blog.Blog).where(models.blog.Blog.id ==
                                            id, models.blog.Blog.user_id == author_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'blog with id {id} was not found')

    return blog


def create_blog(author_id: int, blog: schemas.blog.CreateBlog, db: Session):
    new_blog = models.blog.Blog(
        title=blog.title, body=blog.body, user_id=author_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def upload_cover_image(author_id: int, blog_id: int, cover_img: UploadFile, db: Session):
    blog = get_blog_by_id(blog_id, db)
    if cover_img != None:
        if not os.path.exists(f'{os.path.abspath(os.getcwd())}\\assets\\blog_image'):
            os.makedirs(f'{os.path.abspath(os.getcwd())}\\assets\\blog_image')

        file_path = os.path.join(
            f'{os.path.abspath(os.getcwd())}\\assets\\blog_image', cover_img.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(cover_img.file, buffer)
        blog.cover_image = file_path
        update_blog(author_id, blog.id, blog, db)


def update_blog(author_id: int, blog_id: int, blog_req: schemas.blog.Blog, db: Session):
    blog = db.query(models.blog.Blog).filter(
        models.blog.Blog.id == blog_id, models.blog.Blog.user_id == author_id)
    if not blog.first():
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Blog with id {id} not found")
    blog.update({"cover_image": blog.first().cover_image})
    db.commit()
    return 'updated'


def delete_blog(id: int, db: Session):
    blog = db.query(models.blog.Blog).filter(models.blog.Blog.id == id)
    if not blog.first():
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Blog with id {id} not found")

    blog.delete(synchronize_session=False)
    db.commit()
    return 'deleted'
