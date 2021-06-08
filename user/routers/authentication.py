from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from user import schemas
from user.models.user import User
from user.helpers.hashing import verify_hash
from user.helpers.JWToken import create_access_token
from pydantic import ValidationError


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
        print(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Invalid password validation')
    user = db.query(User).filter(
        User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Invalid credentials')

    if not verify_hash(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Invalid credentials1')

    access_token = create_access_token(
        data={'sub': user.username, 'id': user.id, 'role': user.role})
    return {"access_token": access_token}


@router.get('/confirm/{identifier}')
def confirm_user(identifier: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.user_identifier == identifier)

    if not user.first() or user.first().user_identifier != identifier:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {identifier} was not confirmed')

    user.update({User.is_confirmed: True, User.role: 'user'})
    db.commit()
    raise HTTPException(status_code=status.HTTP_200_OK,
                        detail=f'User with id {identifier} was confirmed')
