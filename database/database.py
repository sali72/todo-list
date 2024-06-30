import os

import pymongo
from dotenv import load_dotenv
from fastapi import HTTPException
from pymongo import errors

load_dotenv()

MONGO_INITDB_DATABASE = os.getenv("MONGO_INITDB_DATABASE")
MONGO_INITDB_ROOT_USERNAME = os.getenv("MONGO_INITDB_ROOT_USERNAME")
MONGO_INITDB_ROOT_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
MONGO_HOST = os.getenv("MONGO_HOST")

MONGO_LOCAL_HOST = os.getenv("MONGO_LOCAL_HOST")
TEST_MODE = os.getenv("TEST_MODE")

if TEST_MODE == "true":
    client = pymongo.MongoClient(host=MONGO_LOCAL_HOST, port=27017)
else:
    client = pymongo.MongoClient(
        host=MONGO_HOST,
        port=27017,
        username=MONGO_INITDB_ROOT_USERNAME,
        password=MONGO_INITDB_ROOT_PASSWORD,
        authSource="admin",
    )
    print("Connected to mongoDB")

db = client[MONGO_INITDB_DATABASE]
todo_collection = db["todo"]
user_collection = db["user"]
# make username unique
user_collection.create_index("username", unique=True)
user_collection.create_index("email", unique=True)
