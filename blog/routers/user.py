from fastapi.param_functions import Security
from fastapi import APIRouter, Depends
from typing import List
from fastapi_mail.fastmail import FastMail
from fastapi_mail.schemas import MessageSchema
from sqlalchemy.orm import Session
from starlette import status
from starlette.background import BackgroundTasks
from starlette.responses import Response
from blog.database import get_db
from blog import schemas
from blog.repository import user_repo
from blog.helpers.oaut2 import get_current_user
from blog.helpers.helper_conf import conf


router = APIRouter(
    prefix='/user',
    tags=['Users']
)


@router.get('/', response_model=List[schemas.user.ShowUser])
def get_all_users(db: Session = Depends(get_db),
                  current_user: schemas.user.User =
                  Security(get_current_user, scopes=['sysadmin', 'admin'])):
    return user_repo.get_all_users(db)


@router.get('/{id}', response_model=schemas.user.ShowUser)
def get_user_by_id(id: int, db: Session = Depends(get_db),
                   current_user: schemas.user.User =
                   Security(get_current_user, scopes=['sysadmin', 'admin', 'user'])):
    return user_repo.get_user_by_id(id, db)


@router.post('/', response_model=schemas.user.ShowUser)
async def create_user(request: schemas.user.CreateUser, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    print(30*'=', request)
    new_user = user_repo.create_user(request, db)
    if new_user:
        message = MessageSchema(
            subject="Fastapi mail module",
            recipients=[new_user.email],
            body=f"""
                <p>Thanks for using Fastapi-mail</p>
                <p><a href="http://127.0.0.1:8000/confirm/{new_user.id}/{request.password}" target="_blank">Confirm here</a></p>
                """,
            subtype="html"
        )

        fm = FastMail(conf)

        background_tasks.add_task(fm.send_message, message)
        return new_user


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
