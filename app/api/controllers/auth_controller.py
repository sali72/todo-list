from bson import ObjectId
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pymongo import CursorType
from pymongo.results import InsertOneResult
from passlib.context import CryptContext
from datetime import timedelta, timezone, datetime
from typing import Union
import os, re
from dotenv import load_dotenv
import jwt
from jwt.exceptions import InvalidTokenError
from zxcvbn import zxcvbn

from app.crud.user_crud import UserCRUD
from models.models import UserModel
from models.schemas import UserSchema

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
MINIMUM_PASSWORD_STRENGTH = int(os.getenv("MINIMUM_PASSWORD_STRENGTH"))


class AuthController:
    
    user_crud = UserCRUD()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    @classmethod
    async def login_user(cls, username: str, password: str) -> str:
        user = await cls.authenticate_user(username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = cls.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return access_token

    @classmethod
    async def register_user(cls, user_schema: UserSchema):
        
        # await cls.__check_password_strength(user_schema.password, user_schema.username)
        hashed_password = cls.pwd_context.hash(user_schema.password)
        
        user_model = UserModel(username=user_schema.username,
                  hashed_password=hashed_password,
                  email=user_schema.email)
        await cls.user_crud.create_one(user_model)
        
        return await cls.login_user(user_schema.username, user_schema.password)

    @classmethod
    async def __check_password_strength(cls, password, username):
        password_policy = await cls.__check_password_policy(password)
        if not password_policy["status"]:
            raise HTTPException(status_code=400, detail=password_policy["message"])
        
        result = zxcvbn(password, user_inputs=[username])
        if result['score'] < MINIMUM_PASSWORD_STRENGTH:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f" Your password is not strong enough, {result['feedback']['suggestions']}"
                )
    
    @classmethod
    async def __check_password_policy(cls, password: str) -> dict:
        if len(password) < 8:
            return {
                "status": False,
                "message": "Password must be at least 8 characters long",
            }
        if re.search("[0-9]", password) is None:
            return {
                "status": False,
                "message": "Password must contain at least one digit",
            }
        if re.search("[A-Z]", password) is None:
            return {
                "status": False,
                "message": "Password must contain at least one uppercase letter",
            }
        if re.search("[a-z]", password) is None:
            return {
                "status": False,
                "message": "Password must contain at least one lowercase letter",
            }
        return {"status": True, "message": "Password is strong"}

    @classmethod
    async def authenticate_user(cls, username: str, password: str):
        user = await cls.get_user_by_username(username)
        if not user:
            return False
        if not cls.verify_password(password, user.hashed_password):
            return False
        return user

    @classmethod
    async def get_user_by_username(cls, username: str):
        user_dict = await cls.user_crud.get_one_by_username_optional(username)
        return UserModel(username=user_dict['username'],
                        hashed_password=user_dict['hashed_password'],
                        email=user_dict['email'])

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def create_access_token(cls, data: dict, expires_delta: Union[timedelta, None] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def auth_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = await AuthController.get_user_by_username(username)
    if user is None:
        raise credentials_exception
    return user



# async def auth_user(current_user: UserSchema = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
#     return current_user
