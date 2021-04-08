from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from jose.exceptions import JWTError
from blog.schemas import token


SECRET_KEY = "29d54264f4b9340762e7d81d523e1a1931802b3bc706a65480e3817b84b0433a"
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


def verify_token(tkn: str, credentials_exception):
    try:
        payload = jwt.decode(tkn, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = token.TokenData(username=username)
    except JWTError:
        raise credentials_exception
