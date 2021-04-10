from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from blog.helpers.hashing import bycrpt_hash
from blog.models import user


def get_all_users(db: Session):
    users = db.query(user.User).all()
    return users


def get_user_by_id(id: int, db: Session):
    usr = db.query(user.User).where(user.User.id == id).first()
    if not usr:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with id {id} was not found')

    return usr


def create_user(user_req: user.User, db: Session):
    new_user = user.User(name=user_req.name, email=user_req.email,
                         username=user_req.username, password=bycrpt_hash(user_req.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
