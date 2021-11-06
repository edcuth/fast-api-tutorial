
from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

from sqlalchemy.sql.sqltypes import TIMESTAMP


# We should have a schema for everything an user should send to the api
# and also for everything we need to send back from the api


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config():
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    class Config():
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

class PostOut(BaseModel):
    Post: Post
    votes: int