from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from blog.helpers.hashing import Hash
from blog import models, schemas


def get_all_users(db: Session):
    users = db.query(models.User).all()
    return users


def get_user_by_id(id: int, db: Session):
    user = db.query(models.User).where(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with id {id} was not found')

    return user


def create_user(user_req: schemas.User, db: Session):
    new_user = models.User(name=user_req.name, email=user_req.email,
                           username=user_req.username, password=Hash.bycrpt(user_req.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
