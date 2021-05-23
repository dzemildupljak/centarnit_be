import os
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.sql import roles
from starlette.background import BackgroundTasks
from starlette.responses import JSONResponse
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from blog.database import get_db
from blog.models.user import User
from blog.helpers.hashing import verify_hash
from blog.helpers.JWToken import create_access_token
from blog.schemas import email
from fastapi_mail import FastMail, MessageSchema
from blog.helpers.helper_conf import conf


router = APIRouter(
    tags=['Authentication']
)

html = """
            <p>Thanks for using Fastapi-mail JA SAM BABOO!!!</p> 
        """


@router.post("/email")
async def simple_send(email: email.EmailSchema):

    message = MessageSchema(
        subject="Fastapi-Mail module",
        # List of recipients, as many as you can pass
        recipients=email.dict().get("email"),
        body=html,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Invalid credentials')

    if not verify_hash(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Invalid credentials1')

    access_token = create_access_token(
        data={'sub': user.username, 'role': user.role})
    return {"access_token": access_token}


@router.get('/confirm/{identifier}/{password}')
def confirm_user(identifier: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.user_identifier == identifier)

    if not user.first() or user.first().password != password or user.first().user_identifier != identifier:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {identifier} was not confirmed')

    user.update({User.is_confirmed: True, User.role: 'user'})
    db.commit()
    raise HTTPException(status_code=status.HTTP_200_OK,
                        detail=f'User with id {identifier} was confirmed')
