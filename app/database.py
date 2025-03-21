import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg.rows import dict_row
from sqlalchemy.orm import Session
import psycopg
load_dotenv()

user = os.getenv("user")
database = os.getenv("dbname")
password = os.getenv("password")
host = os.getenv("host")

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}/{database}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


# db_user = os.getenv("user")
# database = os.getenv("dbname")
# password = os.getenv("password")
# host = os.getenv("host")


# try:
#     conn = psycopg.connect(
#         host=host,
#         dbname=database,
#         user=db_user,
#         password=password,
#         # cursor_factory=RealDictCursor,
#         row_factory=dict_row,
#     )
#     cursor = conn.cursor()
#     print("Database Connection established")
# except Exception as error:
#     print("Error while connecting to the database", error)
