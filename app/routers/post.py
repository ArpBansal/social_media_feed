from fastapi import FastAPI, Response, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import session
from ..db import get_db
from .. import schemas
from .. import models
from typing import List, Optional
from ..oauth2 import get_current_user
from sqlalchemy import func, case, Integer, cast
# from fastapi.encoders import jsonable_encoder

router = APIRouter(tags=['Posts'])

@router.get("/")
def root():
    return {"message": "hi mom"}


@router.get("/posts", response_model= List[schemas.PostOut])
def get_posts(db:session=Depends(get_db), limit:int =5, skip:int=0, search:Optional[str]= ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts=cursor.fetchall() 

    posts = db.query(models.Post, func.sum(case((models.Vote.choice == 1, 1), else_=0)).label('total_likes'),
    func.sum(case((models.Vote.choice==-1, 1), else_=0)).label('total_dislikes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # test_query=db.query(models.Vote.post_id, func.sum(case((models.Vote.choice == 1, 1), else_=0)).label('total_likes'),
    # func.sum(case((models.Vote.choice==-1, 1), else_=0)).label('total_dislikes')).group_by(models.Vote.post_id).all()
    # IT WORKS, OUTPUT is a List [post_id, total_likes, total_dislikes]
        
    # result= jsonable_encoder(tst) 
    
    return posts

@router.post("/posts", status_code=201)
def create_post(post: schemas.PostCreate, db:session=Depends(get_db), current_user:int=Depends(get_current_user)): #payload: dict=Body(...)
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)
    # RETURNING *""",
    # (post.title, post.content, post.published))
    # new_post=cursor.fetchone()
    # conn.commit()
    new_post=models.Post(**post.dict(), user_id=current_user.id)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data": new_post}

# curl -X POST -H "Content-type:application/json" --data "{\"title\":\"waifu_1\", \"content\":\"sakura\"}" http://localhost:8000/posts


'''define a response model'''
@router.get("/posts/latest")
def get_latest_post(db:session=Depends(get_db)):
    # posts = cursor.execute("""SELECT TOP 1 * FROM posts ORDER BY id DESC RETURNING *""")
    posts=db.query(models.Post).order_by(models.Post.id.desc()).first()
    # apply .filter(models.Post.user_id == current_user.id) # get only the user's post
    return {"detail": posts}

@router.get("/posts/{id}")
def get_post(id: int, response: Response,db:session=Depends(get_db), current_user: int=Depends(get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # fetched_post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id==id).first()

    if post is None:
        raise HTTPException(status_code=404, detail=f"post with id:{id} was not found")
        # response.status_code=404
    return {"post_detail": post}

@router.delete("/posts/delete/{id}", status_code=204)
def delete_post(id:int,db:session=Depends(get_db), current_user: int=Depends(get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id))) 
    # delete_post=cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id==id)

    post= post_query.first()

    if post is None:
        raise HTTPException(status_code=404, detail=f"Post with id: {id} not found")
        return

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail="Not authorised to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return {'message': 'post was successfully deleted'} #Response(status_code=status.HTTP_204_NO_CONTENT)
    
@router.put("/posts/update/{id}")
def update_post(id:int, updated_post: schemas.PostCreate, db:session=Depends(get_db), current_user: int = Depends(get_current_user)):
    # cursor.execute("""UPDATE posts SET title= %s, content=%s, published=%s WHERE id=%sRETURNING *""",
    #  (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    # return {"message": "Post updated successfully", "post": updated_post}
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    
    if post is None:
        raise HTTPException(status_code=404, detail=f"Post with id: {id} not found")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail="Not authorised to perform requested action")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

@router.post("/posts/{id}/comment")
def comment(comment:schemas.CreateComment, id:int, db:session=Depends(get_db), current_user:int = Depends(get_current_user)):

    # GETTING COMMENTS
    # query = db.query(models.Comments).filter(
        # models.Comments.post_id == id, models.Comments.user_id == current_user.id).all()
    new_comment = models.Comments(post_id = id, user_id= current_user.id, comment = comment.comment)
    db.add(new_comment)
    db.comment()
    db.refresh(new_comment)

    return new_comment