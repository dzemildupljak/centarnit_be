import os
from user.helpers.JWToken import get_user_id_from_request_jwt
from fastapi.param_functions import Security
from fastapi import APIRouter, Depends
from typing import List
from fastapi_mail.fastmail import FastMail
from fastapi_mail.schemas import MessageSchema
from sqlalchemy.orm import Session
from starlette import status
from starlette.background import BackgroundTasks
from starlette.requests import Request
from starlette.responses import Response
from database import get_db
from user import schemas
from user.repository import user_repo
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
async def create_user(request: schemas.user.CreateUser, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    new_user = user_repo.create_user(request, db)
    if new_user:
        message = MessageSchema(
            subject="Fastapi mail module",
            recipients=[new_user.email],
            body=f"""
                <p>Thanks for using our aplication</p>
                <p>Confirm your account <a href="{HOST_DOMAIN}auth/confirm/{new_user.user_identifier}" target="_blank">here</a></p>
                """,
            subtype="html"
        )

        fm = FastMail(conf)

        background_tasks.add_task(fm.send_message, message)
        return new_user


@router.get('/reset-password/{id}/{email}')
def reset_password(id: int, email: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    usr = user_repo.get_user_by_id(id, db)
    if usr and usr.email == email:
        message = MessageSchema(
            subject="Fastapi mail module",
            recipients=[email],
            body=f"""
                <p>Thanks for using Fastapi-mail</p>
                <p><a href="{HOST_DOMAIN}reset-password/confirm/{usr.user_identifier}" target="_blank">Confirm here</a></p>
                """,
            subtype="html"
        )

        fm = FastMail(conf)
        background_tasks.add_task(fm.send_message, message)
        return usr
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.post('/reset-password/confirm/{identifier}')
def reset_password_confirm(identifier: str,  password: str, password_confirm: str, db: Session = Depends(get_db)):
    if password == password_confirm:
        usr = user_repo.get_user_by_identifier(identifier, db)
        if user_repo.reset_password(usr.id, password, db):
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.put('/', response_model=schemas.user.ShowUser,)
def update_user(request: schemas.user.EditUser, req: Request, db: Session = Depends(get_db),
                current_user: schemas.user.User = Security(get_current_user, scopes=['sysadmin', 'admin', 'user'])):
    if not (user_repo.update_user(get_user_id_from_request_jwt(req), request, db)):
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return user_repo.get_user_by_id(get_user_id_from_request_jwt(req), db)


@router.put('/{id}', response_model=schemas.user.ShowUser,)
def update_any_user(id: int, request: schemas.user.EditUser, db: Session = Depends(get_db),
                    current_user: schemas.user.User = Security(get_current_user, scopes=['sysadmin', 'admin'])):
    if not (user_repo.update_user(id, request, db)):
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return user_repo.get_user_by_id(id, db)


@router.put('/{id}/role/{role}')
def update_user_role(id: int, role: str, db: Session = Depends(get_db),
                     current_user: schemas.user.User = Security(get_current_user, scopes=['sysadmin', 'admin'])):
    return user_repo.update_user_role(id, role, db)


@router.delete('/{id}')
def delete_user(id: int, db: Session = Depends(get_db),
                current_user: schemas.user.User = Security(get_current_user, scopes=['sysadmin', 'admin'])):
    if (user_repo.delete_user(id, db)):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.delete('/hard_delete/{id}')
def delete_user(id: int, db: Session = Depends(get_db),
                current_user: schemas.user.User = Security(get_current_user, scopes=['sysadmin', 'admin'])):
    if (user_repo.hard_delete_user(id, db)):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return Response(status_code=status.HTTP_404_NOT_FOUND)
