from fastapi import APIRouter, Path

from app.api.controllers.auth_controller import AuthController
from models.schemas import ResponseSchema, UserSchema

router = APIRouter(tags=["Authentication"])


@router.post("/register", response_model=ResponseSchema)
async def create_todo_route(user_schema: UserSchema):
    jwt = ""

    message = "User registered successfully"
    data = {"jwt": jwt}
    return ResponseSchema(data=data, message=message)


@router.post("/login", response_model=ResponseSchema)
async def create_todo_route(user_schema: UserSchema):
    jwt = ""

    message = "User logged in successfully"
    data = {"jwt": jwt}
    return ResponseSchema(data=data, message=message)
