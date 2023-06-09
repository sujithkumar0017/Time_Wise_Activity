import models
from database import engine
from fastapi import FastAPI

from routers import posts, users

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)



