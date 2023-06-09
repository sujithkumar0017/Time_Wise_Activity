import json
from typing import List, Optional

from fastapi import FastAPI, HTTPException, APIRouter, Depends ,status,Request
# from fastapi.security import oauth2
import Oauth2
import models
import schemas
from database import SessionLocal
from schemas import Post


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

db = SessionLocal()

@router.get("/", response_model=List[schemas.View_Post])
def get_posts(current_user: int = Depends(Oauth2.get_current_user)):
    posts = db.query(models.post).all()
    return posts


# @router.get("/loginuser")
# def get_post_login_user(current_user: int = Depends(Oauth2.get_current_user)):
#     post = db.query(models.post).filter(models.post.owner_id == current_user.id).all()
#     if not post:
#        raise HTTPException(
#            status_code=400, detail="Post not found")
#     return post

@router.get("/{user_id}")
def get_post_by_user_id(user_id:int):
    get_post = db.query(models.post).filter(models.post.owner_id == user_id).all()
    if not get_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return get_post

@router.post("/",response_model=schemas.View_Post)
def create_post(post:Post,current_user: int = Depends(Oauth2.get_current_user)):
    exist = db.query(models.post).filter(models.post.id == post.id).first()
    if exist:
        raise HTTPException(
            status_code=400, detail="Post already exists")
    new_post = models.post(
       owner_id=current_user.id, **post.dict()
  )
    # print(type(post),"zxccvvcc")
    # print(dict(post),"qwerty123")
    db.add(new_post)
    db.commit()
    create_activity(schemas.UserActivity(
        id= 3,
        entity_id = post.id,
        entity_type = "Post",
        actor = current_user.id,
        raw_data = json.dumps(dict(post)),
        action = "Created"
    ))
    return new_post

# @router.put("/update")
# def update_post(post:Post,current_user: int = Depends(Oauth2.get_current_user)):
#     exist = db.query(models.post).filter(models.post.id == post.id).first()
#     print(type(exist))
#     if not exist:
#         raise HTTPException(status_code=400, detail="Post already exists")
#     values = dict(post)
#     print(values, "####")
#     exist.title = post.post_name
#     exist.content = post.content
#     db.commit()
#     exist = db.query(models.post).filter(models.post.id == post.id).first()
#     values2 = dict(post)
#     print(values2,"$$$$")



def create_activity(activity: schemas.UserActivity):
    new_activity = models.activity(**activity.dict())
    db.add(new_activity)
    db.commit()

def update_activity(dict1,dict2):
 variables = {}
 for key, values in dict1.items():
   if values not in dict2.values():
        variables[key] = values.lower()
   return variables

@router.put("/update")
def update_post(post: Post, current_user: int = Depends(Oauth2.get_current_user)):
        exist = db.query(models.post).filter(models.post.id == post.id).first()

        if not exist:
            raise HTTPException(status_code=400, detail="Post does not exist")

        # Store the original data before updating
        original_data = {
            "id": exist.id,
            "title": exist.post_name,
            "content": exist.content
        }

        # Retrieve the updated data
        updated_data = {
            "id": exist.id,
            "title": post.post_name,
            "content": post.content
        }

        new_post = update_activity(original_data, updated_data)
        exist.title = post.post_name
        exist.content = post.content
        db.commit()

        create_activity(schemas.UserActivity(
            id=9,
            entity_id=post.id,
            entity_type="Post",
            actor=current_user.id,
            raw_data=json.dumps(dict(new_post)),
            action="Edited"
        ))
        return updated_data

