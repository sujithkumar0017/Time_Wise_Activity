from typing import List

from fastapi import FastAPI, HTTPException, status, Request, APIRouter, Depends

import Oauth2
import models
from schemas import User_Register, User_Login, Post
from database import SessionLocal


app = FastAPI()

db = SessionLocal()


router = APIRouter(
    prefix= "/users",
    tags=['Users']
)



# @app.get("/posts/get",response_model=Post)
# def get_posts():
#     posts = db.query(models.post).all()
#     print(posts)
#     return posts


@router.get("/",status_code=status.HTTP_200_OK,response_model=List[User_Register])
def get_users():
    users = db.query(models.user).all()
    return users

@router.post("/",status_code=status.HTTP_201_CREATED,response_model= User_Register)
def create_user(user:User_Register):
    db_item =db.query(models.user).filter(models.user.email == user.email).first()
    # if db_item is None:
    #     raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = Oauth2.hash(user.password)
    user.password = hashed_password
    new_user =models.user(
                name = user.name,
                email = user.email,
                phone = user.phone,
                password = user.password
    )
    print(user.password)
    db.add(new_user)
    db.commit()
    return new_user


@router.get("/{user_id}",status_code=status.HTTP_200_OK,response_model=User_Register)
def get_user_by_id(user_id: int):
    db_item = db.query(models.user).filter(models.user.id == user_id).first()

    if db_item is None:
        raise HTTPException(status_code=400,detail="user not found")
    return db_item

@router.put("/{user_id}",status_code=status.HTTP_200_OK,response_model=User_Register)
def update_user(user_id:int,user:User_Register):
    item_to_update = db.query(models.user).filter(models.user.id == user_id).first()
    item_to_update.name = user.name
    item_to_update.email = user.email
    item_to_update.phone = user.phone
    item_to_update.password = user.password

    db.add(item_to_update)
    db.commit()
    return item_to_update


@router.delete("/{user_id}",status_code=status.HTTP_200_OK,response_model=User_Register)
def delete_user(user_id:int):
    delete_user = db.query(models.user).filter(models.user.id == user_id).first()

    if delete_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")

    db.delete(delete_user)
    db.commit()
    return delete_user


@router.post("/login",status_code=status.HTTP_200_OK)
def get_user(user: User_Login):

    userdata = db.query(models.user).filter(models.user.email == user.email).first()
    print(userdata)
    if userdata is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    if not Oauth2.verify(user.password,userdata.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    access_token = Oauth2.create_access_token(payload={"user_id":userdata.id})
    return {"access_token": access_token,"token_type":"bearer"}

