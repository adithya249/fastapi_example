from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

import models,schemas,database, oauth2 
from database import engine, get_db

router = APIRouter(
    prefix="/vote", tags=['Vote']
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):


    vote_post = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id).first()
    if not vote_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")


    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user{current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)    
        db.add(new_vote)
        db.commit()

        return {"message": "Added vote"}

    else: 
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote doesn't exit")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message":"successfully deleted vote"}