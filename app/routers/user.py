from fastapi import FastAPI, Response, status,HTTPException,APIRouter
import psycopg2 as pg
from psycopg2.extras import RealDictCursor
from .. import schemas, utils
from ..config import settings
from datetime import time

router = APIRouter(prefix="/users")

while True:
    try:
        conn = pg.connect(host=settings.database_hostname,database=settings.database_name,user=settings.database_username,password=settings.database_password,cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("database connection successful")
        break
    except Exception as error:
        print("connecting to databse failed")
        print("Error: ",error)
        time.sleep(2)


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UsersCreatedResponse)
def create_users(user_info:schemas.UsersBase):
    
    hashed_password = utils.password_hasher(user_info.password)
    user_info.password = hashed_password
    cursor.execute("""INSERT INTO users (email,password) VALUES (%s,%s) returning *""",(user_info.email,user_info.password))
    created_user=cursor.fetchone()
    conn.commit()
    return created_user



@router.get("/{id}", response_model=schemas.UsersCreatedResponse)
def get_user(id:int):
    cursor.execute("""SELECT * FROM users WHERE id = %s""",(str(id),))
    user_info = cursor.fetchone()
    if user_info == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"the user with id : {id} does not exist")

    return user_info
