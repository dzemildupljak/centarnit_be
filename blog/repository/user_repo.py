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
                            detail=f'User with id {id} was not found')

    return usr


def create_user(user_req: user.User, db: Session):
    try:
        new_user = user.User(name=user_req.name, email=user_req.email,
                             username=user_req.username, password=bycrpt_hash(
                                 user_req.password), role='')
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Cannot create this user')


def update_user_role(id: int, rle: str, db: Session):
    if rle not in ['admin', 'user', 'author', 'sysadmin']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Cannot assign this role')
    usr = db.query(user.User).filter(
        user.User.id == id)
    if usr.first() and usr.first().role != rle:
        usr.update({user.User.role: rle})
        db.commit()
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f'User with id {id} was updated')
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'User with id {id} was not updated')


def delete_user(id: int, db: Session):
    usr = db.query(user.User).filter(user.User.id == id)
    if not usr.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {id} was not found')
    usr.delete(synchronize_session=False)
    db.commit()
    return True
