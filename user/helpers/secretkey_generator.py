from passlib.context import CryptContext
from secrets import token_bytes, token_hex
from base64 import b64encode

# print(b64encode(token_bytes(32)).decode())
# print(30*'-')
# print(token_hex(32))

# from random import randint
# print(randint(1_000_000, 1_000_000_000_000))


pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated='auto')

sifra = pwd_cxt.hash('sysadmin')
# print(sifra)
