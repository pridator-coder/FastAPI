from fastapi import FastAPI, Response, status,HTTPException,APIRouter, Depends
import psycopg2 as pg
from typing import List, Optional
from psycopg2.extras import RealDictCursor
from .. import schemas,oauth2
from ..config import settings
from datetime import time
router = APIRouter(prefix="/posts")

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




# the -- reload flag is useful in development environment when there will be constant changes and not in production environmet
@router.get("/",response_model=List[schemas.PostResponse])
def get_posts(get_current_user = Depends(oauth2.get_current_user), limit: Optional[int] =100,offset: Optional[int] =0, search: Optional[str] = None):
    if search != None:
        searchpattern1=search+'%'
        searchpattern2='%'+search+'%'
        searchpattern3='%'+search
        cursor.execute("""SELECT * FROM posts WHERE user_id = %s AND (title LIKE %s OR title LIKE %s OR title LIKE %s OR content LIKE %s OR content LIKE %s OR content LIKE %s)  LIMIT %s OFFSET %s""",(get_current_user['id'],searchpattern1,searchpattern2,searchpattern3,searchpattern1,searchpattern2,searchpattern3,int(limit),int(offset)))
        post = cursor.fetchall()
    else:
        cursor.execute("""SELECT * FROM posts WHERE user_id = %s  LIMIT %s OFFSET %s""",(get_current_user['id'],int(limit),int(offset)))
        post = cursor.fetchall()
    # print(posts)
    # return {"data" : posts}
    return post

# when scanning for a code the code stops running at the instance of first match

@router.post("/",status_code=status.HTTP_201_CREATED,response_model = schemas.PostResponse)
def create_posts(post: schemas.PostCreate,get_current_user: int = Depends(oauth2.get_current_user)):
    #print(post.rating)
    #print(post.dict())
    # print(get_current_user)
    cursor.execute("""INSERT INTO posts (title,content,is_published,user_id) VALUES (%s,%s,%s,%s) returning *""",(post.title, post.content,post.is_published,get_current_user['id']))
    new_posts = cursor.fetchone()
    conn.commit()
    # return {"data": new_posts}
    return new_posts

#title str, content str

@router.get("/{id}",response_model=schemas.PostResponse)
# response: Response
def get_post(id:str,get_current_user: int = Depends(oauth2.get_current_user)):
    #print(id)
    # post=find_post(id)
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {id} was not found"}
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    posts=cursor.fetchone()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    # conn.commit()
    #print(posts)
    # return {"post_detail": posts}
    return posts

@router.delete("/{id}")
def delete_post(id:int,get_current_user: int = Depends(oauth2.get_current_user)):
    # index = find_index_post(id)
    # my_posts.pop(index)
    cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),))
    post=cursor.fetchone()
    if get_current_user['id']!=post['user_id']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f"post with id: {id} does not belong to logged in user")
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")
    cursor.execute("""DELETE FROM posts WHERE id = %s and user_id = %s returning *""",(str(id),get_current_user['id']))
    post=cursor.fetchone()
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model=schemas.PostResponse)
def update_post(id:int, post:schemas.PostUpdate,get_current_user: int = Depends(oauth2.get_current_user)):
    # index = find_index_post(id)
    # post_dict=post.dict()
    # post_dict['id']=id
    # my_posts[index]=post_dict
    cursor.execute("""SELECT * FROM posts WHERE id = %s """,((str(id)),))
    updated_post=cursor.fetchone()
    conn.commit()
    if get_current_user['id']!=updated_post['user_id']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f"post with id: {id} does not belong to logged in user")
    if updated_post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")
    cursor.execute("""UPDATE posts SET title = %s, content = %s, is_published = %s WHERE id = %s returning *""",(post.title,post.content,post.is_published,(str(id))))
    updated_post=cursor.fetchone()
    conn.commit()

    # return {'message':updated_post}
    return updated_post



