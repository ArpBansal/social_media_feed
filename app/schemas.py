from pydantic import BaseModel, EmailStr, validator, Field
from datetime import datetime
from typing import Optional, Literal
# from fastapi import Request
# from fastapi.security.oauth2 import OAuth2PasswordRequestForm


# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True
#     rating: Optional[float]=None
class UserOut(BaseModel):
    id:int
    email: EmailStr
    created_at:datetime

    class ConfigDict:
        from_attributes=True

class PostReaction(BaseModel):
    total_likes:int
    total_dislikes:int

class PostBase(BaseModel):
    title:str
    content:str
    published:bool = True
    rating: Optional[float]=None


class PostCreate(PostBase):
    pass

class Post(PostBase):
    id:int
    created_at:datetime
    user_id:int
    posted_by: UserOut
    # total_likes:int
    # total_dislikes:int   

    class ConfigDict:
        from_attributes = True

class PostOut(BaseModel):
    Post: Post
    total_likes: int
    total_dislikes:int

    class ConfigDict:
        from_attributes = True
class PostUpadate(PostBase):
    pass

class UserData(BaseModel):
    email: EmailStr
    password: str
    id:int

class UserCreate(BaseModel):
    email: EmailStr
    password: str




    class ConfigDict:
        from_attributes=True


class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    
class Vote(BaseModel):
    post_id:int
    choice: Literal[1, 0, -1]
    # choice:int = Field(...)

    # @validator('choice', always=True)
    # def check_vote(cls, v):
    #     if v not in (1,0,-1):
    #         raise ValueError('choice must be 1, 0 or -1')

 
# class OAuth2ExtendedForm(OAuth2PasswordRequestForm):
#     def __init__(self, request: Request, user: UserLogin):
#         super().__init__(request)
#         self.email = user.email
#         self.password= user.password
class CreateComment(BaseModel):
    comment: str