from enum import Enum


class TodoModel:

    def __init__(self, description, due_date, status: bool, user_id):
        self.description = description
        self.due_date = due_date
        self.status = status
        self.user_id = user_id


class Role(Enum):
    ADMIN = "admin"
    USER = "user"


class UserModel:

    def __init__(self, username, hashed_password, email, role: Role) -> None:
        self.username = username
        self.hashed_password = hashed_password
        self.email = email
        self.role: Role = role
