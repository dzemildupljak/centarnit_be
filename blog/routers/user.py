from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db
from ..hashing import Hash
from .. import schemas, models
router = APIRouter()


@router.get('/user', response_model=List[schemas.ShowUser], tags=["users"])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get('/user/{id}', response_model=schemas.ShowUser, tags=["users"])
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).where(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with id {id} was not found')

    return user


@router.post('/user', response_model=schemas.ShowUser, tags=["users"])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email,
                           username=request.username, password=Hash.bycrpt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
