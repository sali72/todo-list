from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from dotenv import load_dotenv
import os

from app.api.controllers.auth_controller import AuthController
from models.schemas import ResponseSchema, UserSchema, Token

load_dotenv()

router = APIRouter(tags=["Authentication"])

@router.post("/register", response_model=ResponseSchema)
async def create_todo_route(user_schema: UserSchema):
    access_token = ""

    message = "User registered successfully"
    data = Token(access_token=access_token, token_type="bearer")
    return ResponseSchema(data=data, message=message)


@router.post("/login")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    access_token = await AuthController.login_user(form_data.username, form_data.password)
    
    return Token(access_token=access_token, token_type="bearer")
