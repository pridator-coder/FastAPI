from jose import JWTError, jwt
from datetime import datetime, timedelta,time
from . import schemas
from .config import settings
from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
import psycopg2 as pg
from typing import List
from psycopg2.extras import RealDictCursor

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


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#Secret_key
#ALgorithm
#expiration time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str , credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:str = payload.get("user_id")

        if not id:
            raise credentials_exception
        token_data = schemas.TokenData(id=str(id))
    except JWTError:
        raise credentials_exception
    
    return token_data
    


def get_current_user(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})
    token = verify_access_token(token,credentials_exception)
    cursor.execute("""SELECT * FROM users WHERE id = %s""",(token.id,))
    user = cursor.fetchone()
    return user