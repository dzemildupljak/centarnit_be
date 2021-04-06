from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.orm import Session
from blog.database import get_db
from blog import schemas
from blog.repository import blog_repo
from blog.oaut2 import get_current_user

router = APIRouter(
    prefix='/blog',
    tags=['Blog']
)


@router.get('/', response_model=List[schemas.ShowBlog])
def get_all_blogs(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return blog_repo.get_all_blogs(db)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def get_blog_by_id(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return blog_repo.get_blog_by_id(id, db)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.CreateBlog, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return blog_repo.create_blog(request, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return blog_repo.update_blog(id, request, db)


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return blog_repo.delete_blog(id, db)
