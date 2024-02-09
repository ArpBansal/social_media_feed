from .. import models, schemas, utils
from fastapi import FastAPI, Response, HTTPException, status, Depends, APIRouter
from ..db import get_db
from sqlalchemy.orm import session
from typing import List

router = APIRouter(
    # '''TODO   prefix'''
    tags=['Users'])

'''Don't include in final API'''
@router.get("/userdata", response_model=List[schemas.UserData])
def userdata(db:session = Depends(get_db)):
    userdata = db.query(models.Users).with_entities(
        models.Users.id, models.Users.email, models.Users.password).all()
    # converting each tuple to a UserCreate object
    # userdata = [schemas.UserData(id=id, email=email, password=password) for id, email, password in userdata]
    return userdata # return the list of UserCreate objects
    
@router.post("/signin", status_code=201, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db:session = Depends(get_db)):
    hash_password = utils.hash(user.password)
    user.password = hash_password

    new_user = models.Users( **user.dict())
    db.add(new_user)
    db.commit()
    return new_user
    # db.refresh(new_user)
        
@router.get(('/user/{id}'), response_model=schemas.UserOut)
def get_user(id:int, db:session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == str(id)).first()
    if user is None:
        raise HTTPException(status_code=404,
        detail=f"user with id: {id} does not exist")

    return user