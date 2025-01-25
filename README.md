# FastAPI Basic Auth

A simple and flexible Basic Authentication middleware for FastAPI applications.

## Installation

```bash
pip install fastapi-basic-auth
```

## Usage

### Basic Usage with Dictionary

```python
from fastapi import FastAPI
from fastapi_basic_auth import FastAPIBasicAuthMiddleware

app = FastAPI()

# Add middleware
auth = FastAPIBasicAuthMiddleware(
    urls=["/protected"],
    users={"admin": "password"}
)
app.add_middleware(auth.build)

@app.get("/protected")
def protected():
    return {"message": "This route is protected"}
```

### Using BasicAuthUser Model

You can also use the `BasicAuthUser` model directly for more control and validation:

```python
from fastapi import FastAPI
from fastapi_basic_auth import FastAPIBasicAuthMiddleware, BasicAuthUser

app = FastAPI()

# Create users using BasicAuthUser model
users = [
    BasicAuthUser(username="admin", password="password123"),
    BasicAuthUser(username="user1", password="userpass")
]

# Add middleware with BasicAuthUser list
auth = FastAPIBasicAuthMiddleware(
    urls=["/protected", "/admin"],  # Protect multiple routes
    users=users
)
app.add_middleware(auth.build)

@app.get("/protected")
def protected():
    return {"message": "This route is protected"}

@app.get("/admin")
def admin():
    return {"message": "Admin route is protected"}
```

The `BasicAuthUser` model includes built-in validation:
- Username must be alphanumeric (can include underscores and hyphens)
- Both username and password are required fields

## Features

- Protect specific routes with Basic Authentication
- Support for multiple users
- Flexible configuration
  - Use simple dictionary for quick setup
  - Use BasicAuthUser model for additional validation
- Secure password comparison