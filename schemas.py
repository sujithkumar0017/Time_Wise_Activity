from typing import Optional, Dict, Any

from pydantic import BaseModel, EmailStr, json


class User_Register(BaseModel):
    # id: int
    name: str
    email: EmailStr
    phone: int
    password: str

    class Config:
        orm_mode = True

class User_Login(BaseModel):
        email: EmailStr
        password: str

        class Config:
            orm_mode = True

class Post(BaseModel):
    id:int
    post_name: str
    content: str

class View_Post(Post):
    owner_id: int
    owner: User_Login

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id:Optional[str] = None

class UserActivity(BaseModel):
    id:int
    entity_id : int
    entity_type: str
    raw_data: str
    actor: int
    action: str


    class Config:
        orm_mode = True