from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List

from .. import database, models, schemas, utils,  oauth2

router = APIRouter(
    prefix="/votes",
    tags=['Votes']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post does not exist.")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    current_vote = vote_query.first()
    if(vote.direction == 1):
        if current_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Already liked.")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"vote added"}
    else:
        if not current_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Already deleted.")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"vote deleted"}