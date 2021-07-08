import datetime
from typing import Optional
from user.helpers.oaut2 import get_current_user

from fastapi.param_functions import Security
from user.helpers.helpers import generate_ot_confirmation_code, get_time_between
from user.repository import user_repo
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from user import schemas
from user.models.user import User
from user.helpers.hashing import verify_hash
from user.helpers.JWToken import create_access_token
from pydantic import ValidationError
import msgpack

router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)


# html = """
#             <p>Thanks for using Fastapi-mail TEST MAIL!!!</p>
#         """
# @router.post("/email")
# async def simple_send(email: email.EmailSchema):

#     message = MessageSchema(
#         subject="Fastapi-Mail module",
#         # List of recipients, as many as you can pass
#         recipients=email.dict().get("email"),
#         body=html,
#         subtype="html"
#     )

#     fm = FastMail(conf)
#     await fm.send_message(message)
#     return JSONResponse(status_code=200, content={"message": "email has been sent"})


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        schemas.user.Login(
            username=request.username,
            password=request.password
        )
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Invalid password validation')
    user = db.query(User).filter(
        User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Invalid credentials123')

    if not verify_hash(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Invalid credentials1')

    access_token = create_access_token(
        data={'sub': user.username, 'id': user.id, 'role': user.role})
    return {"access_token": access_token}


@router.get('/mail/{email}/confirm/{identifier}')
def confirm_user(email: str, identifier: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.email == email)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {identifier} was not confirmed')
    if generate_ot_confirmation_code(user.first().created_at) != identifier:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {identifier} was not confirmed')
    user.update({User.is_confirmed: True, User.role: 'user'})
    db.commit()
    raise HTTPException(status_code=status.HTTP_200_OK,
                        detail=f'User with id {identifier} was confirmed')


@router.get('/confirm/code/{confirmation_code}')
def confirm_user_by_code(confirmation_code: str, username: Optional[str] = None,
                         email: Optional[str] = None,  db: Session = Depends(get_db),
                         current_user: schemas.user.User = Security(get_current_user, scopes=['undefined'])):
    if username:
        usr = user_repo.get_user_by_username(username, db)
    else:
        usr = user_repo.get_user_by_username(email, db)
    try:
        with open('stream.msgpack', 'rb+') as f:
            load_items = [item for item in msgpack.Unpacker(f)]
            f.truncate(0)
    except:
        pass

    for i in load_items:
        if (i['email'] == usr.email
                and get_time_between(datetime.datetime.strptime(i['time'], "%Y-%m-%d %H:%M:%S.%f"), datetime.datetime.now()) < 60
                and i['code'] == confirmation_code):
            del i
            user_repo.update_user_role(usr.id, 'user', db)
    with open('stream.msgpack', 'wb') as f:
        for i in load_items:
            f.write(msgpack.packb(i))

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'User was not updated')
