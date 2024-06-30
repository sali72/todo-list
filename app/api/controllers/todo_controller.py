from bson import ObjectId
from fastapi import HTTPException
from pymongo import CursorType
from pymongo.results import InsertOneResult

from app.crud.todo_crud import TodoCRUD
from models.models import TodoModel
from models.schemas import TodoSchema


class TodoController:

    todo_crud = TodoCRUD()

    @classmethod
    async def create_todo(cls, todo_schema: TodoSchema) -> str:
        todo_model = await cls.__create_todo_model(todo_schema)
        result: InsertOneResult = await cls.todo_crud.create_todo(todo_model)
        return str(result.inserted_id)

    @classmethod
    async def get_all_todo(cls) -> dict:
        all_todo_cursor = await cls.todo_crud.get_all()

        return cls.__pymongo_cursor_to_dict(all_todo_cursor)

    @classmethod
    async def get_one_todo(cls, _id: str) -> dict:
        objectId = cls.__validate_input_OID(_id)

        todo_dict = await cls.todo_crud.get_one_by_id(objectId)
        return cls.__format_dict_id(todo_dict)

    @classmethod
    async def update_one_todo(cls, todo_id: str, todo_schema: TodoSchema) -> str:
        OID = cls.__validate_input_OID(todo_id)
        base_todo = await cls.todo_crud.get_one_by_id(OID)

        cls.__check_input_for_update(todo_schema, base_todo)

        todo_model = await cls.__create_todo_model(todo_schema)

        await cls.todo_crud.update_one(OID, todo_model)
        return str(base_todo["_id"])

    @classmethod
    async def delete_one_todo(cls, todo_id: str) -> str:
        OID = cls.__validate_input_OID(todo_id)

        await cls.todo_crud.delete_one(OID)
        return todo_id

    @classmethod
    async def __create_todo_model(cls, todo_schema: TodoSchema) -> TodoModel:
        return TodoModel(
            description=todo_schema.description,
            due_date=todo_schema.due_date,
            status=todo_schema.status,
        )

    @classmethod
    def __remove_id_from_dict(cls, dict: dict) -> dict:
        dict.pop("_id")
        return dict

    @classmethod
    def __pymongo_cursor_to_dict(cls, cursor: CursorType) -> dict:
        list_items = list(cursor)
        return {
            str(item["_id"]): cls.__remove_id_from_dict(item) for item in list_items
        }

    @classmethod
    def __format_dict_id(cls, dict: dict) -> dict:
        return {str(dict["_id"]): cls.__remove_id_from_dict(dict)}

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
