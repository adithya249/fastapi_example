from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
#from .. import models, schemas, utils
#from ..database import engine, get_db
from sqlalchemy.orm import Session


import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

import models,schemas,utils, database
from database import engine, get_db



router = APIRouter(prefix="/users",tags=['Users'])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate,db: Session = Depends(get_db)):
    
    #hash the pwd - user.password
    #hashed_password = pwd_context.hash(user.password)
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())

    #commit changes for them to be reflected in the database
    db.add(new_user)
    db.commit() 
    db.refresh(new_user)
 
    return new_user


@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id: int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} doesn't exist")

    return user    