from datetime import datetime, timedelta
from fastapi import Depends
from fastapi import Depends, HTTPException ,status,Request
from fastapi.security import OAuth2PasswordBearer
# import datetime

from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import database
import models
import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# import schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


#hash the password

def hash(password:str):
    return pwd_context.hash(password)

def verify(plain_passsword,hashed_password):
    return pwd_context.verify(plain_passsword,hashed_password)


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(payload: dict):
    to_encode = payload.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encode_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    print(encode_jwt)
    return encode_jwt
def verify_access_token(token: str,credentials_exception):
   #while executing the code sometime it make error so we use try expect block.
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        print(f'payload: {payload}')
        id:str =payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    print(token_data,"iiiiiii")
    return token_data
# pass this method as dependency injection of the path operations ,it will take the token from the request automatically, it verify the token whether it is correct or not using verify access token
def get_current_user(db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    print(f'token: {token}')
    credentials_expection = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Could not validate credentials",headers={"WWW-Authentication":"Bearer"})
    token = verify_access_token(token,credentials_expection)
    user = db.query(models.user).filter(models.user.id == token.id).first()

    return user