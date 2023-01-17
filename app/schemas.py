from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(Post):
    pass

class PostUpdate(Post):
    pass

class PostResponse(Post):
    id: int
    created_at: datetime
    user_id: int
    owner: UserOut

    class Config:
        orm_mode = True

class PostWithVotes(BaseModel):
    Post: PostResponse
    votes: int

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]

class Vote(BaseModel):
    post_id: int
    direction: conint(le=1)