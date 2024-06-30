from bson import ObjectId
from pymongo.results import DeleteResult, InsertOneResult, UpdateResult

from commons.exception_handler import (ensure_delete_one_found,
                                       ensure_find_one_found,
                                       ensure_update_modified)
from database.database import user_collection
from models.models import UserModel


class UserCRUD:

    def __init__(self) -> None:
        self.user_collection = user_collection

    async def create_one(self, user_model: UserModel) -> InsertOneResult:
        user_dict = user_model.__dict__
        self.__remove_id_before_creation(user_dict)
        return self.user_collection.insert_one(user_dict)

    def __remove_id_before_creation(self, user_dict):
        if "_id" in user_dict:
            del user_dict["_id"]

    async def get_all(self):
        return self.user_collection.find({})
    
    @ensure_find_one_found("User")
    async def get_one_by_username(self, username: str) -> dict:
        return self.user_collection.find_one({"username": username})

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
                    "role": user_model.role
                }
            },
        )

    @ensure_delete_one_found("User")
    async def delete_one(self, _id: ObjectId) -> DeleteResult:
        return self.user_collection.delete_one({"_id": _id})
