from fastapi import APIRouter, Depends

from app.api.controllers.auth_controller import has_role
from app.api.controllers.todo_controller import TodoController
from models.models import Role as R
from models.schemas import ResponseSchema, TodoSchema

router = APIRouter(prefix="/todo", tags=["TODO"])


@router.post("", response_model=ResponseSchema)
async def create_todo_route(todo_schema: TodoSchema, user=Depends(has_role(R.USER))):
    _id = await TodoController.create_todo(todo_schema, user)

    message = "Todo task created successfully"
    data = {"id": _id}
    return ResponseSchema(data=data, message=message)


@router.get("", response_model=ResponseSchema)
async def get_all_todo_route(user=Depends(has_role(R.USER))):
    todos = await TodoController.get_all_todo(user)

    message = "All tasks retrieved successfully"
    return ResponseSchema(data=todos, message=message)


@router.get("/{id}", response_model=ResponseSchema)
async def get_todo_route(id: str, user=Depends(has_role(R.USER))):
    todo = await TodoController.get_one_todo(id, user)

    message = "Todo task retrieved successfully"
    return ResponseSchema(data=todo, message=message)


@router.put("/{id}", response_model=ResponseSchema)
async def update_todo_route(id: str, todo_schema: TodoSchema, user=Depends(has_role(R.USER))):
    _id = await TodoController.update_one_todo(id, todo_schema, user)

    message = "Todo task updated successfully"
    data = {"id": _id}
    return ResponseSchema(data=data, message=message)


@router.delete("{id}", response_model=ResponseSchema)
async def create_todo_route(id: str, user=Depends(has_role(R.USER))):
    _id = await TodoController.delete_one_todo(id)

    message = "Todo task deleted successfully"
    data = {"id": _id}
    return ResponseSchema(data=data, message=message)
