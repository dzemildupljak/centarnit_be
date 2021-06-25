from user.helpers.JWToken import get_user_id_from_request_jwt
from fastapi import APIRouter, Depends, status
from typing import List
from fastapi.param_functions import Security
from sqlalchemy.orm import Session
from starlette.requests import Request
from database import get_db
from blog.schemas import blog
from user.schemas import user
from blog.repository import blog_repo
from user.helpers.oaut2 import get_current_user

router = APIRouter(
    prefix='/blog',
    tags=['Blog']
)


@router.get('/', response_model=List[blog.ShowBlog])
def get_all_blogs(db: Session = Depends(get_db)):
    return blog_repo.get_all_blogs(db)


@router.get('/my_blogs', response_model=List[blog.ShowBlog])
def get_all_my_blogs(req: Request, db: Session = Depends(get_db),
                     current_user: user.User =
                     Security(get_current_user, scopes=['sysadmin', 'admin', 'user'])):
    return blog_repo.get_all_blogs_by_author(get_user_id_from_request_jwt(req), db)


@router.get('/id/{id}', status_code=status.HTTP_200_OK, response_model=blog.ShowBlog)
def get_blog_by_id(id: int, req: Request, db: Session = Depends(get_db),
                   current_user: user.User =
                   Security(get_current_user, scopes=['sysadmin', 'admin', 'user'])):
    return blog_repo.get_blog_by_id(id, get_user_id_from_request_jwt(req), db)


@router.get('my/id/{id}', status_code=status.HTTP_200_OK, response_model=blog.ShowBlog)
def get_my_blog_by_id(id: int, req: Request, db: Session = Depends(get_db),
                      current_user: user.User =
                      Security(get_current_user, scopes=['sysadmin', 'admin', 'user'])):
    return blog_repo.get_my_blog_by_id(id, get_user_id_from_request_jwt(req), db)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_blog(request: blog.CreateBlog, req: Request, db: Session = Depends(get_db),
                current_user: user.User =
                Security(get_current_user, scopes=['sysadmin', 'admin', 'user'])):
    return blog_repo.create_blog(get_user_id_from_request_jwt(req), request, db)


@router.put('/{blog_id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(blog_id: int,  request_data: blog.UpdateBlog, req: Request, db: Session = Depends(get_db),
                current_user: user.User =
                Security(get_current_user, scopes=['sysadmin', 'admin', 'user'])):
    return blog_repo.update_blog(get_user_id_from_request_jwt(req), blog_id, request_data, db)


@router.delete('/{blog_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(blog_id: int, req: Request, db: Session = Depends(get_db),
                current_user: user.User =
                Security(get_current_user, scopes=['sysadmin', 'admin', 'user'])):
    return blog_repo.delete_blog(get_user_id_from_request_jwt(req), blog_id, db)
