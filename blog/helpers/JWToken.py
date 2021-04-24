from datetime import datetime, timedelta
from typing import Optional
from fastapi.exceptions import HTTPException
from fastapi.security.oauth2 import SecurityScopes
from jose import jwt
from jose.exceptions import JWTError
from starlette import status
from dotenv.main import dotenv_values


SECRET_KEY = dotenv_values()['SECRET_KEY']
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(tkn: str, role: SecurityScopes):
    try:
        payload = jwt.decode(tkn, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        rls = payload.get("role")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if rls not in role.scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this location",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
