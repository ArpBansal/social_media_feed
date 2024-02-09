from fastapi import FastAPI, Response, HTTPException, status, Depends, APIRouter
from sqlalchemy import and_

from sqlalchemy.orm import session
from ..db import get_db
from .. import schemas, models
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.get("/data", status_code=200)
def get_vote_data(db:session=Depends(get_db)):
    data = db.query(models.Vote).all()
    return data

@router.post("/", status_code=status.HTTP_201_CREATED)
def like_dislike(vote:schemas.Vote, db:session=Depends(get_db), current_user:int = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {vote.post_id} does not exist")

    vote_query = db.query(models.Vote).filter(models.Post.id==vote.post_id, models.Vote.user_id==current_user.id)
    
    # subquery = db.query(models.Vote.post_id).join(models.Post, models.Post.id == models.Vote.post_id).filter(
    # models.Vote.post_id == vote.post_id,
    # models.Vote.user_id == current_user.id).subquery()

    # vote_query = db.query(models.Vote).filter(models.Vote.post_id.in_(subquery))

    
    # v_user_query= db.query(models.Vote).join(models.Post,models.Post.id==vote.post_id).filter(
    #  models.Post.id==vote.post_id, models.Vote.user_id==current_user.id)
    v_user= db.query(models.Vote).filter(
     models.Vote.post_id==vote.post_id, models.Vote.user_id==current_user.id).first()



    match vote.choice:
        case 1:
            if v_user is None:
                new_vote= models.Vote(post_id=vote.post_id, user_id=current_user.id, choice=1)
                db.add(new_vote)
                db.commit()

            elif(v_user.choice==-1):
                    vote_query.update({models.Vote.choice: vote.choice}, synchronize_session=False)
                    db.commit()
            else:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
             detail=f"user {current_user.id} has already liked on post {vote.post_id}")

        case 0:
            vote_query.delete(synchronize_session=False)
            db.commit()

        case -1:
            if v_user is None:
                new_vote= models.Vote(post_id=vote.post_id, user_id=current_user.id, choice=-1)
                db.add(new_vote)
                db.commit()

            elif(v_user.choice==1):
                    vote_query.update({models.Vote.choice: vote.choice}, synchronize_session=False)
                    db.commit()
            else:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
             detail=f"user {current_user.id} has already disliked on post {vote.post_id}")