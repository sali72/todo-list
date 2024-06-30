from bson import ObjectId
from pymongo.results import DeleteResult, InsertOneResult, UpdateResult

from commons.exception_handler import (ensure_delete_one_found,
                                       ensure_find_one_found,
                                       ensure_update_modified)
from database.database import todo_collection
from models.models import TodoModel


class TodoCRUD:

    def __init__(self) -> None:
        self.todo_collection = todo_collection

    async def create_todo(self, todo_model: TodoModel) -> InsertOneResult:
        return self.todo_collection.insert_one(todo_model.__dict__)

    async def get_all(self):
        return self.todo_collection.find({})

    @ensure_find_one_found("Task")
    async def get_one_by_id(self, _id: ObjectId) -> dict:
        return self.todo_collection.find_one({"_id": _id})

    @ensure_update_modified("Task")
    async def update_one(self, _id: ObjectId, todo_model: TodoModel) -> UpdateResult:
        return self.todo_collection.update_one(
            {"_id": _id},
            {
                "$set": {
                    "description": todo_model.description,
                    "due_date": todo_model.due_date,
                    "status": todo_model.status,
                }
            },
        )

    @ensure_delete_one_found("Task")
    async def delete_one(self, _id: ObjectId) -> DeleteResult:
        return self.todo_collection.delete_one({"_id": _id})
