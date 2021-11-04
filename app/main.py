from os import stat
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from sqlalchemy import engine
from sqlalchemy.orm import Session, session
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schema
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#run uvicorn main:app --reload to start the web server

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


@app.get("/")
async  def root():
    return {"message": "Hello world"}

@app.get('/posts')
async def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"posts": posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_post(post: schema.PostCreate):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"message": new_post}

@app.get('/posts/{id}')
async def get_post_by_id(id: int):
    cursor.execute("""SELECT * FROM posts where id = %s""", (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id {id} not found")
    return {"post_detail": post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
async def update_post(id: int, post: schema.PostCreate):
    cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, id))
    post = cursor.fetchone()
    conn.commit()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    return {"message":f"post {id} updated", "post":post}

@app.get("/sqlalchemy/posts")
async def orm_get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.post("/sqlalchemy/posts", status_code=status.HTTP_201_CREATED)
def orm_create_post(post: schema.PostCreate, db: session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {'new post': new_post}


@app.get("/sqlalchemy/posts/{id}")
async def orm_get_post( id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} not found')
    return {'post': post}

@app.delete('/sqlalchemy/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def orm_delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} not found')
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/sqlalchemy/posts/{id}")
async def orm_update_post(id: int, updated_post: schema.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} not found')
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return {'updated post': post_query.first()}