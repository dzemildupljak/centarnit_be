from fastapi.param_functions import Security
from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from starlette import status
from blog.database import get_db
from blog import schemas
from blog.repository import user_repo
from blog.helpers.oaut2 import get_current_user


router = APIRouter(
    prefix='/user',
    tags=['Users']
)


@router.get('/', response_model=List[schemas.user.ShowUser])
def get_all_users(db: Session = Depends(get_db),
                  current_user: schemas.user.User =
                  Security(get_current_user, scopes=['sysadmin', 'admin'])):
    return user_repo.get_all_users(db)


@router.get('/{id}', response_model=schemas.user.ShowUser)
def get_user_by_id(id: int, db: Session = Depends(get_db),
                   current_user: schemas.user.User =
                   Security(get_current_user, scopes=['sysadmin', 'admin'])):
    return user_repo.get_user_by_id(id, db)


@router.post('/', response_model=schemas.user.ShowUser)
def create_user(request: schemas.user.User, db: Session = Depends(get_db)):
    return user_repo.create_user(request, db)


@router.put('/{id}/role/{role}')
def update_user_role(id: int, role: str, db: Session = Depends(get_db)):
    return user_repo.update_user_role(id, role, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db),
                current_user: schemas.user.User =
                Security(get_current_user, scopes=['sysadmin', 'admin'])):
    return user_repo.delete_user(id, db)
