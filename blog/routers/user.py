from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from blog.database import get_db
from blog import schemas
from blog.repository import user_repo
from blog.helpers.oaut2 import get_current_user


router = APIRouter(
    prefix='/user',
    tags=['Users']
)


@router.get('/', response_model=List[schemas.ShowUser])
def get_all_users(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return user_repo.get_all_users(db)


@router.get('/{id}', response_model=schemas.ShowUser)
def get_user_by_id(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return user_repo.get_user_by_id(id, db)


@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user_repo.create_user(request, db)
