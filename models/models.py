class TodoModel:

    def __init__(self, description, due_date, status: bool):
        self.description = description
        self.due_date = due_date
        self.status = status


class UserModel:

    def __init__(self, username, hashed_password, email) -> None:
        self.username = username
        self.hashed_password = hashed_password
        self.email = email
