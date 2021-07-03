import os
import uuid
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from user.helpers.hashing import bycrpt_hash
from jose import jwt
from user.models import user

SECRET_KEY = str(os.getenv('SECRET_KEY'))
ALGORITHM = str(os.getenv('ALGORITHM'))
ACCESS_TOKEN_EXPIRE_MINUTES = str(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))


def get_all_users(db: Session):
    users = db.query(user.User).all()
    return users


def get_all_active_users(db: Session):
    users = db.query(user.User).filter(user.User.is_active == True).all()
    return users


def get_user_by_id(id: int, db: Session):
    usr = db.query(user.User).where(user.User.id == id).first()
    if not usr:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {id} was not found')

    return usr


def get_user_by_email(email: str, db: Session) -> user.User:
    usr = db.query(user.User).where(user.User.email == email).first()
    if not usr:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User was not found')

    return usr


def get_user_by_username(username: str, db: Session) -> user.User:
    usr = db.query(user.User).where(user.User.username == username).first()
    if not usr:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User was not found')

    return usr


def get_current_user_by_id(user_id: int, db: Session):
    usr = db.query(user.User).where(user.User.id == user_id).first()
    if not usr:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {user_id} was not found')

    return usr


def get_user_by_identifier(identifier: int, db: Session):
    usr = db.query(user.User).where(
        user.User.user_identifier == identifier).first()
    if not usr:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User was not found')

    return usr


def create_user(user_req: user.User, db: Session):
    ################### remove in production with alembic migrations ##########
    if not get_user_by_username('sysadmin', db):
        new_sysadmin = user.User(name='sysadmin', email='sysadmin@mail.com',
                                 username='sysadmin', password=bycrpt_hash(
                                     'sysadmin'), role='', user_identifier=str(uuid.uuid1()))
        db.add(new_sysadmin)
    ################### remove in production with alembic migrations ##########

    try:
        new_user = user.User(name=user_req.name, email=user_req.email,
                             username=user_req.username, is_active=True, password=bycrpt_hash(
                                 user_req.password), role='', user_identifier=str(uuid.uuid1()))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        if new_user:
            return new_user
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Cannot create this user')
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Cannot create this user')


def update_user_role(id: int, rle: str, db: Session):
    if rle not in ('admin', 'user', 'author'):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Cannot assign this role')
    usr = db.query(user.User).filter(
        user.User.id == id, user.User.role != rle).update({user.User.role: rle})
    print(30*'=', usr)
    if not usr:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {id} was not updated')
    db.commit()
    raise HTTPException(status_code=status.HTTP_200_OK,
                        detail=f'User with id {id} was updated')


def update_user(id: int, updated_user,  db: Session):
    usr = db.query(user.User).filter(
        user.User.id == id).update(dict(updated_user))

    if not usr:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {id} was not found')
    db.commit()
    return True


def reset_password(id: int, new_password,  db: Session):
    usr = db.query(user.User).filter(user.User.id == id)
    if not usr.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {id} was not found')
    usr.update({user.User.password: new_password})
    db.commit()
    return True


def code_reset_password(code: int, new_password,  db: Session):
    usr = db.query(user.User).filter(user.User.id == id)
    if not usr.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {id} was not found')
    usr.update({user.User.password: new_password})
    db.commit()
    return True


def delete_user(id: int, db: Session):
    usr = db.query(user.User).filter(
        user.User.id == id).update({user.User.is_active: False})
    if not usr:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {id} was not found')
    db.commit()
    return usr


def hard_delete_user(id: int, db: Session):
    usr = db.query(user.User).filter(user.User.id == id)
    if not usr.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {id} was not found')
    usr.delete(synchronize_session=False)
    db.commit()
    return True
