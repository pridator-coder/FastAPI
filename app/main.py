from fastapi import FastAPI, Response, status,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional,List
# from random import randrange
# import psycopg2 as pg
# from psycopg2.extras import RealDictCursor
# import time
# from . import schemas, utils
from .routers import post, user,auth, vote


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#path operation
@app.get("/")   #http method that needs to be put after the url to see the message from function below
async def root():    #an asynchronous function definition
    return {"message": "Welcome to my first api!!!"}

# while True:
#     try:
#         conn = pg.connect(host='localhost',database='FastAPI',user='postgres',password='1234',cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("database connection successful")
#         break
#     except Exception as error:
#         print("connecting to databse failed")
#         print("Error: ",error)
#         time.sleep(2)


# my_posts = [{"title":"title of post 1", "content": "content of post 1", "id":1},{"title":"fav foods","content": "My fav food is maggi", "id":2}]

# def find_post(id):
#     for i in my_posts:
#         if i['id'] == id:
#             return i


# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#        if p['id']==id:
#             return i


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)