from pydantic import BaseModel
from pydantic.class_validators import validator


class User(BaseModel):
    name: str
    email: str
    username: str
    password: str
    role: str
    is_active: bool


class CreateUser(BaseModel):
    name: str
    email: str
    username: str
    password: str

    @validator('password')
    def password_must_contain_nums_letters(cls, password: str):
        if len(password) < 5:
            raise ValueError('must contain more than 5 characters')
        if not any(chr.isalnum for chr in password):
            raise ValueError('must contain only leter and digit')
        if not any(chr.isdigit for chr in password):
            raise ValueError(f'must contain a digit')
        return password

    # class Config:
    #     orm_mode = True

    #     @validator('name')
    # def name_must_contain_space(cls, v):
    #     if ' ' not in v:
    #         raise ValueError('must contain a space')
    #     return v.title()

    # @validator('password2')
    # def passwords_match(cls, v, values, **kwargs):
    #     if 'password1' in values and v != values['password1']:
    #         raise ValueError('passwords do not match')
    #     return v

    # @validator('username')
    # def username_alphanumeric(cls, v):
    #     assert v.isalnum(), 'must be alphanumeric'
    #     return v


class EditUser(BaseModel):
    name: str
    email: str
    username: str

    class Config:
        orm_mode = True


class ShowActiveUser(BaseModel):
    id: int
    name: str
    email: str
    username: str
    role: str
    is_active: bool

    class Config:
        orm_mode = True


class ShowUser(BaseModel):
    id: int
    name: str
    email: str
    username: str
    role: str

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str

    @validator('password')
    def password_must_contain_nums_letters(password):
        if password == "sysadmin":
            return password
        if len(password) < 5:
            raise ValueError('must contain more than 5 characters')
        if any(chr.isalnum() for chr in password):
            raise ValueError('must contain only letter and digits')
        if any(chr.isdigit() for chr in password):
            raise ValueError('must contain a digit')
        return password

    class Config:
        orm_mode = True
