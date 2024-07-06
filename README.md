# todo-list

**## Task Management System API**

This API provides a simple platform for managing user tasks, adhering to CRUD (Create, Read, Update, Delete) operations. It leverages a JWT (JSON Web Token) system for authentication and authorization, ensuring data integrity and access control.

**Features:**

- User Management: Create, retrieve, update, and delete user accounts.
- Task Management: Create, retrieve, update, and delete tasks associated with users.
- Secure Authentication: Implements JWT for authentication, safeguarding user data.
- Role-Based Authorization: Enforces access control based on user roles (e.g., admin, user).
- Flexible Data Storage: Utilizes MongoDB for scalable and efficient data persistence.

**Database Structure:**

The API employs two primary MongoDB collections:

* **users:** Stores user information, including username, email, hashed password (for security), and role (for authorization).
* **todos:** Stores task details, comprising a unique identifier (`_id`), description, due date (`due_date`), completion status (`status`), and a foreign key reference (`user_id`) linking the task to its corresponding user.

**Example Documents:**

* **User:**

```json
{
  "_id": {
    "$oid": "66817f697bb309e6542cca32"
  },
  "username": "john",
  "email": "johndoe@example.com",
  "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
  "role": "admin"
}
```

* **Todo:**

```json
{
  "_id": {
    "$oid": "66817dbf51a88dcc6187f2c6"
  },
  "description": "string",
  "due_date": {
    "$date": "2024-06-30T15:53:11.872Z"
  },
  "status": false,  // Boolean indicating completion status (false = incomplete)
  "user_id": {
    "$oid": "667fdc6c08718eac4d0fe26c"
  }
}
```

**API Usage:**

The API provides a set of endpoints (URLs) for interacting with user and task data. Refer to the detailed API documentation (swagger api doc runs at /docs in your running server)

**Authentication:**

1. Register a user to obtain a JWT token.
2. Include the JWT token in the authorization header of subsequent API requests for authentication.
