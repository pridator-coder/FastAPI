from fastapi import FastAPI, Response, status,HTTPException,APIRouter,Depends
from .. import schemas,oauth2
import psycopg2 as pg
from psycopg2.extras import RealDictCursor
from ..config import settings
from datetime import time
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

router = APIRouter()
@router.post("/vote",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.VoteIn, get_current_user = Depends(oauth2.get_current_user)):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (vote.post_id,))
    found_post = cursor.fetchone()
    if not found_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The post with id: {vote.post_id} does not exist")
    
    cursor.execute("""SELECT * FROM votes WHERE user_id = %s AND post_id = %s""", (get_current_user['id'],vote.post_id))
    found_vote = cursor.fetchone()
    if (vote.vote_dir==1):
        if not found_vote:
            cursor.execute("""INSERT INTO votes (post_id,user_id) VALUES (%s,%s) returning *""",(vote.post_id,get_current_user['id']))
            post_detail = cursor.fetchone()
            conn.commit()
            raise HTTPException(status_code=status.HTTP_201_CREATED,detail=f"The user with user id: {get_current_user['id']} has voted in favour of post with post id: {vote.post_id}")        
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"The user with user id: {get_current_user['id']} has already voted in favour of post with post id: {vote.post_id}")        
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"The user with user id: {get_current_user['id']} has never voted in favour of post with post id: {vote.post_id}")        
        else:
            cursor.execute("""DELETE FROM votes WHERE post_id = %s AND user_id = %s returning *""",(vote.post_id,get_current_user['id']))
            conn.commit()
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail=f"the vote was deleted successfully")
    