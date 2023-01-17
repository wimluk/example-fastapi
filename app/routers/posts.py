from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import Optional, List

from .. import database, models, schemas, utils,  oauth2

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostWithVotes])

def get_posts(db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""):
    
    # Users can access only posts for authorized current user:
    # posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()
    
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    postsWithVotes = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return postsWithVotes


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)

def create_posts(post: schemas.PostCreate, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
#    new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(user_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.PostWithVotes)

def get_post(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    # Users can access only posts for authorized current user:
    # post = db.query(models.Post).filter(models.Post.user_id == current_user.id)
    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id: {id} found")
    # if post.user_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)

def delete_posts(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    current_post = post_query.first()
    if not current_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id: {id} found.")
    if current_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.PostResponse)

def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    current_post = post_query.first()
    if not current_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id: {id} found")
    if current_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
