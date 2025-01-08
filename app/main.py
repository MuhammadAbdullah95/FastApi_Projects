import os
from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import Union, Optional
from fastapi.params import Body
from pydantic import BaseModel
import psycopg
from psycopg.rows import dict_row
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Load environment variables from.env file
load_dotenv()

user = os.getenv("user")
database = os.getenv("dbname")
password = os.getenv("password")
host = os.getenv("host")


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


try:
    conn = psycopg.connect(
        host=host,
        dbname=database,
        user=user,
        password=password,
        # cursor_factory=RealDictCursor,
        row_factory=dict_row,
    )
    cursor = conn.cursor()
    print("Database Connection established")
except Exception as error:
    print("Error while connecting to the database", error)

# while True:
#     try:
#         with psycopg.connect(
#             host="localhost",
#             dbname="fastapi",
#             user="postgres",
#             password="AB31405",
#             row_factory=dict_row,
#         ) as conn:
#             with conn.cursor() as cursor:
#                 print("Database Connection established")
#                 break
#     except Exception as error:
#         print("Error while connecting to the database", error)
#         time.sleep(3)


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()
    return {"data": post}


# Getting all posts from database
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}


# Insert a new post into the database using POST method
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"body": new_post}


# Getting single post from database with it's id using get method
@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (id,))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: '{id}' not found",
        )
    return {"data": post}


# Delete a post using delete method with post id
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: '{id}' not found",
        )

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# updating a post by using put method with post id
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET title = %s, content = %s , published = %s WHERE id = %s RETURNING *""",
        (post.title, post.content, post.published, id),
    )
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: '{id}' not found",
        )
    return {"data": updated_post}
