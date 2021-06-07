from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated='auto')


def bycrpt_hash(password: str):
    return pwd_cxt.hash(password)


def verify_hash(plain_password, hashed_password):
    return pwd_cxt.verify(plain_password, hashed_password)
