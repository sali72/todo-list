from bson import ObjectId
from fastapi import HTTPException
from pymongo import CursorType
from pymongo.results import InsertOneResult

from app.crud.todo_crud import TodoCRUD
from app.crud.user_crud import UserCRUD
from models.models import TodoModel, UserModel
from models.schemas import TodoSchema


class TodoController:

    todo_crud = TodoCRUD()
    user_crud = UserCRUD()

    @classmethod
    async def create_todo(cls, todo_schema: TodoSchema, user: UserModel) -> str:
        todo_model = await cls.__create_todo_model(todo_schema, user._id)
        result: InsertOneResult = await cls.todo_crud.create_todo(todo_model)
        return str(result.inserted_id)

    @classmethod
    async def get_all_todo(cls, user: UserModel) -> dict:
        all_todo_cursor = await cls.todo_crud.get_all_by_user_id(user._id)

        return cls.__pymongo_cursor_to_dict(all_todo_cursor)

    @classmethod
    async def get_one_todo(cls, _id: str, user: UserModel) -> dict:
        task_oid = cls.__validate_input_OID(_id)
        user_oid = cls.__validate_input_OID(user._id)

        todo_dict = await cls.todo_crud.get_one_by_task_and_user_id(task_oid, user_oid)
        return cls.__format_dict_id(todo_dict)

    @classmethod
    async def update_one_todo(
        cls, todo_id: str, todo_schema: TodoSchema, user: UserModel
    ) -> str:
        task_oid = cls.__validate_input_OID(todo_id)
        user_oid = cls.__validate_input_OID(user._id)
        base_todo = await cls.todo_crud.get_one_by_task_and_user_id(task_oid, user_oid)

        cls.__check_input_for_update(todo_schema, base_todo)

        todo_model = await cls.__create_todo_model(todo_schema, user_oid)

        await cls.todo_crud.update_one(task_oid, todo_model)
        return str(base_todo["_id"])

    @classmethod
    async def delete_one_todo(cls, todo_id: str, user: UserModel) -> str:
        task_oid = cls.__validate_input_OID(todo_id)
        user_oid = cls.__validate_input_OID(user._id)

        await cls.todo_crud.delete_one_by_task_and_user_id(task_oid, user_oid)
        return todo_id

    @classmethod
    async def __create_todo_model(
        cls, todo_schema: TodoSchema, user_id: str
    ) -> TodoModel:
        return TodoModel(
            description=todo_schema.description,
            due_date=todo_schema.due_date,
            status=todo_schema.status,
            user_id=user_id,
        )

    @classmethod
    def __process_dict(cls, dict: dict) -> dict:
        cls.user_oid_to_str(dict)
        return cls.__remove_id_from_dict(dict)

    @classmethod
    def __remove_id_from_dict(cls, dict):
        dict.pop("_id")
        return dict

    @classmethod
    def user_oid_to_str(cls, dict):
        dict["user_id"] = str(dict["user_id"])

    @classmethod
    def __pymongo_cursor_to_dict(cls, cursor: CursorType) -> dict:
        list_items = list(cursor)
        return {str(item["_id"]): cls.__process_dict(item) for item in list_items}

    @classmethod
    def __format_dict_id(cls, dict: dict) -> dict:
        return {str(dict["_id"]): cls.__process_dict(dict)}

    @classmethod
    def __validate_input_OID(cls, _id: str) -> ObjectId:
        try:
            objectId = ObjectId(_id)
        except:
            raise HTTPException(404, "Wrong id format")
        return objectId

    @classmethod
    def __check_input_for_update(cls, todo_schema, base_todo):
        cls.__check_if_description_update(todo_schema, base_todo)
        cls.__check_if_due_date_update(todo_schema, base_todo)
        cls.__check_if_status_update(todo_schema, base_todo)

    @classmethod
    def __check_if_description_update(cls, update_todo: TodoSchema, base_todo: dict):
        if update_todo.description is None or update_todo.description.strip() == "":
            update_todo.content = base_todo["description"]

    @classmethod
    def __check_if_due_date_update(cls, update_todo: TodoSchema, base_todo: dict):
        if update_todo.due_date is None:
            update_todo.due_date = base_todo["due_date"]

    @classmethod
    def __check_if_status_update(cls, update_todo: TodoSchema, base_todo: dict):
        if update_todo.status is None:
            update_todo.status = base_todo["status"]
