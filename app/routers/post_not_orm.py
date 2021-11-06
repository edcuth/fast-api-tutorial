from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schema
from typing import List
import time
import psycopg2
from psycopg2.extras import RealDictCursor

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='postgres123', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB conn succesfull")
        break
    except Exception as error:
        print('DB conn failed')
        print(error)
        time.sleep(2)
    
router = APIRouter(
    #this variable allows us to remove repeated text from the path
    prefix='/posts',
    #the tags variable will let us separate our stuff by groups
    tags=['posts_without_orm']
)



@router.get('/', response_model=List[schema.Post])
async def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.Post)
async def create_post(post: schema.PostCreate):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return new_post

@router.get('/{id}', response_model=schema.Post)
async def get_post_by_id(id: int):
    cursor.execute("""SELECT * FROM posts where id = %s""", (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id {id} not found")
    return post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', response_model=schema.Post)
async def update_post(id: int, post: schema.PostCreate):
    cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, id))
    post = cursor.fetchone()
    conn.commit()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    return post