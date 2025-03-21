from fastapi import FastAPI
from dotenv import load_dotenv
from . import models
from .database import engine
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Load environment variables from.env file
load_dotenv()


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
