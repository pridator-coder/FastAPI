from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint
# class Post(BaseModel):
#     title:str
#     content:str
#     published: bool = True

# class CreatePost(BaseModel):
#     title:str
#     content:str
#     published: bool = True
# class UpdatePost(BaseModel):
#     title:str
#     content:str
#     published: bool = True

class PostBase(BaseModel):
    title:str
    content:str
    is_published: bool = True

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class PostResponse(PostBase):
    id:int
    created_at:datetime
    user_id: int

class UsersBase(BaseModel):
    email:EmailStr
    password:str
    
class UsersCreatedResponse(BaseModel):
    id: int
    email:EmailStr
    created_at:datetime

class UserLogIn(BaseModel):
    email:EmailStr
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None

class VoteIn(BaseModel):
    post_id: int
    vote_dir: int

