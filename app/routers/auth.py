from .. import models, schemas, utils, oauth2
from fastapi import FastAPI, Response, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import session
from ..db import get_db
# from fastapi.security.oauth2 import OAuth2PasswordRequestForm
 
router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials:schemas.UserLogin, db:session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.email == user_credentials.email).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    #creating a token and returning it
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"token": access_token, "token_type":"bearer"}
