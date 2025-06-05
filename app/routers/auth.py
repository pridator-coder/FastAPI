from fastapi import APIRouter,status,HTTPException,Response,Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import psycopg2 as pg
from typing import List
from psycopg2.extras import RealDictCursor
from .. import schemas,utils, oauth2
from ..config import settings
from datetime import time
router = APIRouter()

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



@router.post("/login",response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    cursor.execute("""SELECT * FROM users WHERE email = %s""",(user_credentials.username,))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail = f"invalid credentials")
    verifi = utils.verify(user_credentials.password,user['password'])
    if not verifi:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail = f"invalid credentials")
    # cursor.execute("""SELECT * FROM users WHERE email = %s AND password = %s""",(user_credentials.email,entered_password_hashed))
    # password = cursor.fetchone()
    # if not password:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"invalid credentials2")
    access_token=oauth2.create_access_token(data = {"user_id":user['id']})
    return {"access_token":access_token,"token_type":"bearer"}