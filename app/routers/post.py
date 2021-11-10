from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schema, oauth2
from ..database import get_db
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    #this variable allows us to remove repeated text from the path
    prefix='/posts',
    #the tags variable will let us separate our stuff by groups
    tags=['posts']
)

@router.get("/", response_model=List[schema.PostOut])
async def orm_get_posts(db: Session = Depends(get_db), 
current_user:int = Depends(oauth2.get_current_user),
limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    #for query parameters, you need to add them as parameters for the function,
    #then send them as part of the url, adding a ? plus the name of the parameter
    #after the endpoint, to add more parameters, use "&" plus the name of the parameter
    # for spaces, use %20 in the url

    # to query all posts
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    #  to query only posts the user owns
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    
    # This is how to join using ORM, keep in mind that the columns from the selected table will be inside
    # a new object named after the table ('Post' in this case), and the count func as another field
    # outside of the object
    results = db.query(models.Post, func.count(
        models.Votes.post_id).label("votes")).join(
            models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(
                models.Post.id).filter(
                    models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return results

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def orm_create_post(post: schema.PostCreate, db: Session = Depends(get_db), 
current_user:int = Depends(oauth2.get_current_user)):
    # Get user ID from their token (get_current_user) and add it to the new post
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schema.PostOut)
async def orm_get_post( id: int, db: Session = Depends(get_db), 
current_user:int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(
        models.Votes.post_id).label("votes")).join(
            models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(
                models.Post.id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} not found')
    return post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def orm_delete_post(id: int, db: Session = Depends(get_db), 
current_user:int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} not found')
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Not authorized to perform requested action')

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schema.Post)
async def orm_update_post(id: int, updated_post: schema.PostCreate, 
db: Session = Depends(get_db), 
current_user:int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} not found')
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Not authorized to perform requested action')
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
