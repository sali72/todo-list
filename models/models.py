class TodoModel:

    def __init__(self, description, due_date, status: bool):
        self.description = description
        self.due_date = due_date
        self.status = status
        
class UserModel:
    
    def __init__(self, username, password, email) -> None:
        self.username = username
        self.password = password
        self.email = email
