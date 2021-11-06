from os import stat
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from sqlalchemy import engine
from sqlalchemy.orm import Session, session
from . import models, schema, utils
from .database import engine, get_db
from .routers import post, user, post_not_orm, auth

models.Base.metadata.create_all(bind=engine) #initiates the tables models

app = FastAPI()

#run uvicorn main:app --reload to start the web server

app.include_router(post.router)
app.include_router(user.router)
app.include_router(post_not_orm.router)
app.include_router(auth.router)

@app.get("/")
async  def root():
    return {"message": "Hello world"}