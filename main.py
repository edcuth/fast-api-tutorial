from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel


app = FastAPI()

#run uvicorn main:app --reload to start the web server

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    id: int = None

my_posts = [{"title": "title1", "content":"some content", "id":1}, {"title":"title2", "conntent":"some other content", "id":2}]

@app.get("/")
async  def root():
    return {"message": "Hello world"}

@app.get('/posts')
async def get_posts():
    return {"posts": my_posts}


@app.post('/posts')
async def create_post(post: Post):
    post.id = len(my_posts) + 1
    my_posts.append(post.dict())
    return {"message": "New Post", "id":post.id}

@app.get('/posts/{id}')
async def get_post_by_id(id: int):
    return {"post": my_posts[id-1]}