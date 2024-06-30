from datetime import datetime
from pydantic import BaseModel, Extra, Field
from passlib.context import CryptContext
class BaseModelConfigured(BaseModel):
    """
    Adds configuration to base model to use for all schemas.

    Configurations:
    forbid extra fields
    """
    class Config:
        extra = Extra.forbid


class TodoSchema(BaseModelConfigured):
    description: str = Field(None, title="The task description")
    due_date: datetime = Field(None, title="The due date for the task")
    status: bool = Field(False, title="The current status of the task")
    
class ResponseSchema(BaseModelConfigured):
    message: str = Field(None, example=" task done successfully ")
    status: str = Field("success", example="success")
    data: dict = Field(None, example={"id": "666ef095c65d183a71a06935"})
    timestamp: datetime = Field(datetime.now(), example="2024-02-16T14:05:09.252968")
    
class UserSchema(BaseModelConfigured):
    username: str = Field(None, title="The task description")
    email: str = Field(None, title="The task description")
    password: str = Field(None, title="The task description")
    
class Token(BaseModel):
    access_token: str
    token_type: str
