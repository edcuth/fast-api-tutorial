from fastapi import FastAPI
from sqlalchemy import engine
from . import models
from .database import engine
from .routers import post, user, post_not_orm, auth, vote
from .config import settings


models.Base.metadata.create_all(bind=engine) #initiates the table models

app = FastAPI()

#run uvicorn main:app --reload to start the web server

app.include_router(post.router)
app.include_router(user.router)
app.include_router(post_not_orm.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async  def root():
    return {"message": "Hello world"}