from bson import ObjectId
from pymongo.results import DeleteResult, InsertOneResult, UpdateResult

from commons.exception_handler import (ensure_delete_one_found,
                                       ensure_update_modified,
                                       ensure_find_one_found)
from database.database import user_collection
from models.models import UserModel


class UserCRUD:

    def __init__(self) -> None:
        self.user_collection = user_collection

    async def create_one(self, user_model: UserModel) -> InsertOneResult:
        return self.user_collection.insert_one(user_model.__dict__)

    async def get_all(self):
        return self.user_collection.find({})

    async def get_one_by_username_optional(self, username: str) -> dict:
        return self.user_collection.find_one({"username": username})
    
    @ensure_find_one_found("User")
    async def get_one_by_id(self, _id: ObjectId) -> dict:
        return self.user_collection.find_one({"_id": _id})

    @ensure_update_modified("User")
    async def update_one(self, _id: ObjectId, user_model: UserModel) -> UpdateResult:
        return self.user_collection.update_one(
            {"_id": _id},
            {
                "$set": {
                    "username": user_model.username,
                    "password": user_model.hashed_password,
                    "email": user_model.email,
                }
            },
        )

    @ensure_delete_one_found("User")
    async def delete_one(self, _id: ObjectId) -> DeleteResult:
        return self.user_collection.delete_one({"_id": _id})
