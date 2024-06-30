import re

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pymongo.errors import DuplicateKeyError

from app.api.endpoints.authentication_routes import router as auth_routes
from app.api.endpoints.todo_routes import router as todo_routes

app = FastAPI()

app.include_router(todo_routes)
app.include_router(auth_routes)


@app.exception_handler(DuplicateKeyError)
async def duplicate_key_error_handler(request, exc):
    # Extract field name from error message
    match = re.search(r'index: (\w+)_', str(exc))
    field_name = match.group(1) if match else "unknown"
    
    return JSONResponse(
        status_code=400,
        content={"error": f"{field_name} already exists."},
    )
