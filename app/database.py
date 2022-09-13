from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import psycopg2
from psycopg2.extras import RealDictCursor
import time

from app.config import settings



SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
  
Base = declarative_base() #all models that we define to create our tables in postgres will be extending this base class

def get_db():
    db = SessionLocal()
    try: 
        yield db 
    finally: 
        db.close() 




#content below not needed as we've made use of sqlalchemy for database connection to postgres. Used to run raw sql through postgres
# while True:

# #realdictcursor lets you know which column name is mapped to which value
#     try: 
#         conn   = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='adithya2000',cursor_factory=RealDictCursor) 
#         cursor = conn.cursor()
#         print("database connection successful") 
#         break
#     except Exception as error:
#         print("connection failed")
#         print(error)
#         time.sleep(2)        
