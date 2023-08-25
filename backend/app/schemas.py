from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from pydantic.types import conint


class UserBase(BaseModel):
    email: str
    password: str

class UserCreate(UserBase):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id : Optional[int] = None

class Message(BaseModel):
    message: str