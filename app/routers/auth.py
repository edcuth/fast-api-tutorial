from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schema, models, utils, oauth2

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login', response_model=schema.Token)
async def login_user(user_credentials: OAuth2PasswordRequestForm = Depends(), 
                    db: Session = Depends(database.get_db)):
    # OAauth2PasswordRequestForm object has fields:
    # username
    # password
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    # login requests should send the credentials as form data instead of raw json
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid Credentails')

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid Credentials')
    
    # Create token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    # return token
    return {"access_token": access_token, "token_type":"bearer"}