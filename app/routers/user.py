from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schema, utils
from ..database import get_db

router = APIRouter(
    #this variable allows us to remove repeated text from the path
    prefix="/users",
    #the tags variable will let us separate our stuff by groups
    tags=['users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
async def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    # hash user.password
    new_user = db.query(models.User).filter(models.User.email == user.email).first()
    if new_user:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'mail already registered')
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schema.UserOut)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not found')
    
    return user

