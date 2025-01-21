import os
from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import Union, Optional, List
from fastapi.params import Body
from pydantic import BaseModel
import psycopg
from psycopg.rows import dict_row
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Load environment variables from.env file
load_dotenv()

db_user = os.getenv("user")
database = os.getenv("dbname")
password = os.getenv("password")
host = os.getenv("host")


try:
    conn = psycopg.connect(
        host=host,
        dbname=database,
        user=db_user,
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


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


# Getting all posts from database
