from fastapi import FastAPI

from app.api.endpoints.todo_routes import router as todo_routes
from app.api.endpoints.authentication_routes import router as auth_routes

app = FastAPI()

app.include_router(todo_routes)
app.include_router(auth_routes)
