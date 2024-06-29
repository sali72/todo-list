from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from dotenv import load_dotenv
import os

from app.api.controllers.auth_controller import authenticate_user, create_access_token
from models.schemas import ResponseSchema, UserSchema, Token

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

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

@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
