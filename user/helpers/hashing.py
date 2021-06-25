import datetime
import random
import math
import os
from time import sleep
from passlib.context import CryptContext
from passlib.hash import oracle10
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY_CODE = str(os.getenv('SECRET_KEY_CODE'))

pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated='auto')


def bycrpt_hash(password: str):
    return pwd_cxt.hash(password)


def verify_hash(plain_password, hashed_password):
    return pwd_cxt.verify(plain_password, hashed_password)
