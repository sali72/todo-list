from bson import ObjectId
from fastapi import HTTPException
from pymongo import CursorType
from pymongo.results import InsertOneResult

from app.crud.todo_crud import TodoCRUD
from models.models import TodoModel
from models.schemas import TodoSchema



class AuthController:
    pass