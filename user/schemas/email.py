from typing import List
from pydantic import BaseModel
from pydantic.networks import EmailStr


class EmailSchema(BaseModel):
    email: List[EmailStr]
