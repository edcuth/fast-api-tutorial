from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import engine
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings


# models.Base.metadata.create_all(bind=engine) #initiates the table models


#run uvicorn main:app --reload to start the web server


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async  def root():
    return {"message": "This 'Hello world' has been pushed with CD!"}