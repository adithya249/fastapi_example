from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
#from .. import models, schemas
#from ..database import engine, get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import delete, func


import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

import models,schemas,database, oauth2 
from database import engine, get_db



router = APIRouter(prefix="/posts", tags=['Posts'])

#response model needs to return a list of our schema posts
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user),limit: int = 5, skip: int = 0, search: Optional[str] = ""):
    #cursor.execute(""" SELECT * FROM post """)
    #posts = cursor.fetchall()
    #print(posts)
    #return {"data": my_db} 
    
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id== models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() #left outer (isouter=true) join
    #print(results)

    return posts


@router.get("/{post_id}",response_model=schemas.PostOut)
def get_post(post_id: int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    #print(post_id)

   # cursor.execute(""" SELECT * from post WHERE id = %s """, (str(post_id)))
   # post = cursor.fetchone()
    #post = find_post(post_id)
   # print(post)
   
   #post = db.query(models.Post).filter(models.Post.id == post_id).first()
   
   post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id== models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == post_id).first()
   
   
   
   #print(post)
   
   
   if not post:
        #response.status_code = 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
   return post 

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    #print (payload)
    #return {"new_post": f"title: {payload['title']} content: {payload['title']}"}
    #print(post)
    #print(post.dict())

   # cursor.execute(""" INSERT INTO post (title, content, published) VALUES (%s,%s,%s) RETURNING * """, (post.title,post.content,post.published))
   # new_post = cursor.fetchone()
   # conn.commit() 
   
    #print(current_user.email)
   # new_post = models.Post(title=post.title, content=post.content,published=post.published)

   # instead of referencing each col separately, convert post to dict and unpack it
    new_post = models.Post(owner_id = current_user.id, **post.dict())

    #commit changes for them to be reflected in the database
    db.add(new_post)
    db.commit() 
    db.refresh(new_post)

    return new_post


    #post_dict = post.dict()
    #post_dict['id'] = randrange(0,1000000)
    #my_db.append(post_dict)
    #return {"data": post_dict}

#title str, content str (user send) 

#delete

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    #find index in the array that has req ID 
    #my_db.pop

   # cursor.execute(""" DELETE FROM post WHERE id = %s returning *""",(str(post_id),))
    #index = find_index_post(post_id)
   # deleted_post = cursor.fetchone()
   # conn.commit()
   

    
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    
    post = post_query.first()


    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id{post_id} doesnt exist")
        
    if post.owner_id != current_user.id:
            
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")    
        
    
    post_query.delete(synchronize_session=False)
        
   #delete_post.delete(synchronize_session=False)
    db.commit() 

   
    #my_db.pop(index)
    #return {'message':"post deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#update 
  
@router.put("/{post_id}", response_model= schemas.PostResponse)
def update_post(post_id: int, updated_post: schemas.PostCreate, db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s 
    #RETURNING *""",
    #              (post.title,post.content,post.published, str(post_id)))
    #updated_post =  cursor.fetchone()
    #conn.commit()
    #index = find_index_post(post_id)

    


    #updated_post = db.query(models.Post).filter(models.Post.id == post_id).update(dict(post))
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()


    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id{post_id} doesnt exist")

    if post.owner_id != current_user.id: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    #updated_post.update(post.dict(),synchronize_session=False) 
    
    post_query.update(updated_post.dict(),synchronize_session=False)
    
    
    db.commit()      
        
    #post_dict = post.dict()
    #post_dict['id'] = post_id 
    #my_db[index] = post_dict
    return post_query.first()
