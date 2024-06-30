from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.controllers.auth_controller import AuthController
from models.schemas import ResponseSchema, Token, UserSchema

load_dotenv()

router = APIRouter(tags=["Authentication"])


@router.post("/register", response_model=ResponseSchema)
async def create_todo_route(user_schema: UserSchema):
    access_token = await AuthController.register_user(user_schema)

    message = "User registered successfully"
    data = Token(access_token=access_token, token_type="bearer")
    return ResponseSchema(data=data, message=message)


@router.post("/login")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    access_token = await AuthController.login_user(
        form_data.username, form_data.password
    )

    return Token(access_token=access_token, token_type="bearer")
