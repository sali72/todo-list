from fastapi import FastAPI

from app.api.endpoints.todo_routes import router as todo_routes

app = FastAPI()

app.include_router(todo_routes)
