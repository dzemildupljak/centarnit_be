from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import SecurityScopes
from user.helpers.JWToken import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", scopes='')


def get_current_user(role: SecurityScopes, token: str = Depends(oauth2_scheme)):
    return verify_token(token, role)
