

from operator import ge, le
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from pydantic.types import conint #for o/1

class Post(BaseModel):
    title: str
    content: str
    published: bool = True 

class PostCreate(Post):
    pass

class PostResponse(Post):
    
    id: int
    created_at: datetime
    owner_id: int

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: PostResponse
    votes: int


class UserCreate(BaseModel):
    email: EmailStr 
    password: str    

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str 
    
class Token(BaseModel):
    access_token: str
    token_type: str   

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int 
    dir: int = Field(None,ge=0,le=1)
