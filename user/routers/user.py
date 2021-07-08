import os
from user.helpers.helpers import generate_ot_confirmation_code
from fastapi.exceptions import HTTPException
from pydantic.error_wrappers import ValidationError
from user.helpers.JWToken import get_user_id_from_request_jwt
from fastapi.param_functions import Security
from fastapi import APIRouter, Depends
from typing import List, Optional
from fastapi_mail.fastmail import FastMail
from fastapi_mail.schemas import MessageSchema
from sqlalchemy.orm import Session
from starlette import status
from starlette.background import BackgroundTasks
from starlette.requests import Request
from starlette.responses import Response
from database import get_db
from user import schemas
from user.repository import confirmation_repo, user_repo
from user.helpers.oaut2 import get_current_user
from user.helpers.helper_conf import conf

HOST_DOMAIN = os.getenv('HOST_DOMAIN')

router = APIRouter(
    prefix='/user',
    tags=['Users']
)


@router.get('/all', response_model=List[schemas.user.ShowActiveUser])
def get_all_users(db: Session = Depends(get_db),
                  current_user: schemas.user.User =
                  Security(get_current_user, scopes=['sysadmin', 'admin'])):
    return user_repo.get_all_users(db)


@router.get('/all/active', response_model=List[schemas.user.ShowActiveUser])
def get_all_active_users(db: Session = Depends(get_db),
                         current_user: schemas.user.User =
                         Security(get_current_user, scopes=['sysadmin', 'admin'])):
    return user_repo.get_all_active_users(db)


@router.get('/{id}', response_model=schemas.user.ShowUser)
def get_user_by_id(id: int, req: Request, db: Session = Depends(get_db),
                   current_user: schemas.user.User =
                   Security(get_current_user, scopes=['sysadmin', 'admin', 'user'])):
    return user_repo.get_user_by_id(id, db)


@router.get('/current/', response_model=schemas.user.ShowUser)
def get_current_logged_user(req: Request, db: Session = Depends(get_db),
                            current_user: schemas.user.User =
                            Security(get_current_user, scopes=['sysadmin', 'admin', 'user'])):
    return user_repo.get_current_user_by_id(get_user_id_from_request_jwt(req), db)


@router.post('/', response_model=schemas.user.ShowUser)
async def create_user(request: schemas.user.CreateUser, db: Session = Depends(get_db)):
    try:
        schemas.user.CreateUser(
            name=request.name,
            email=request.email,
            username=request.username,
            password=request.password

        )
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Invalid login validation')
    new_user = user_repo.create_user(request, db)
    if new_user:
        return new_user


@router.get('/confirm-user/email/{email}')
def req_confirmation_by_email(email: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    usr = user_repo.get_user_by_email(email, db)
    if not usr:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Invalid validation')
    message = MessageSchema(
        subject="Fastapi mail module",
        recipients=[usr.email],
        body=f"""
                <p>Thanks for using our aplication</p>
                <p>Confirm your account <a href="{HOST_DOMAIN}auth/mail/{usr.email}/confirm/{generate_ot_confirmation_code(usr.user_identifier)}" target="_blank">here</a></p>
                """,
        subtype="html"
    )

    fm = FastMail(conf)

    background_tasks.add_task(fm.send_message, message)


@router.get('/confirm-user/code/')
def req_confirmation_by_code(email: Optional[str] = None, username: Optional[str] = None, db: Session = Depends(get_db)):
    return confirmation_repo.req_confirmation_generator(email if email else username, db)


@ router.put('/', response_model=schemas.user.ShowUser,)
def update_user(request: schemas.user.EditUser, req: Request, db: Session = Depends(get_db),
                current_user: schemas.user.User = Security(get_current_user, scopes=['sysadmin', 'admin', 'user'])):
    if not (user_repo.update_user(get_user_id_from_request_jwt(req), request, db)):
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return user_repo.get_user_by_id(get_user_id_from_request_jwt(req), db)


@ router.put('/{id}', response_model=schemas.user.ShowUser,)
def update_any_user(id: int, request: schemas.user.EditUser, db: Session = Depends(get_db),
                    current_user: schemas.user.User = Security(get_current_user, scopes=['sysadmin', 'admin'])):
    if not (user_repo.update_user(id, request, db)):
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return user_repo.get_user_by_id(id, db)


@ router.put('/{id}/role/{role}')
def update_user_role(id: int, role: str, db: Session = Depends(get_db),
                     current_user: schemas.user.User = Security(get_current_user, scopes=['sysadmin', 'admin'])):
    return user_repo.update_user_role(id, role, db)


@ router.delete('/{id}')
def delete_user(id: int, db: Session = Depends(get_db),
                current_user: schemas.user.User = Security(get_current_user, scopes=['sysadmin', 'admin'])):
    if (user_repo.delete_user(id, db)):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@ router.delete('/hard_delete/{id}')
def hard_delete_user(id: int, db: Session = Depends(get_db),
                     current_user: schemas.user.User = Security(get_current_user, scopes=['sysadmin', 'admin'])):
    if (user_repo.hard_delete_user(id, db)):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return Response(status_code=status.HTTP_404_NOT_FOUND)
