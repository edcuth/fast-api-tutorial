from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm.session import Session
from .. import schema, database, models, oauth2

router = APIRouter(
    tags=['Vote'],
    prefix='/vote'
)

@router.post('/', status_code=status.HTTP_201_CREATED)
async def vote(vote: schema.Vote, db: Session = Depends(database.get_db),
current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {vote.post_id} does nt exit')

    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)
    found_vote = vote_query.first()
    if (vote.dir == 1): # to add a vote
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'user {current_user.id} has already voted on post {vote.post_id}')
        new_vote = models.Votes(post_id = vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"successfully added vote"}
    else: # remove vote
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'vote does not exist')
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"successfully deleted vote"}
        