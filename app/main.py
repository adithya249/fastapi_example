from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange


#from passlib.context import CryptContext



from database import engine, get_db
from sqlalchemy.orm import Session
import models, schemas, utils

from routers import post,user,auth, vote
from config import settings


  
    


#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
models.Base.metadata.create_all(bind=engine)

app = FastAPI()



#create a dependency (everytime you get a req, you get a session to the db)
#creates a session to the db so that we can perform operations and then close the session omce req is done
#keep calling function everytime you get a req to your api endpoints




#dummy function:
def find_post(id):
    for p in my_db:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_db):
        if p['id'] == id:
            return i



#class Post(BaseModel):
 #   title: str
  #  content: str
   # published: bool = True 





my_db = [{"title": "twat","content": "prick", "id": 1},
    {"title": "sobby", "content": "twat","id": 2}]



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message":"oi"}
