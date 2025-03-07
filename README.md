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
app.add_middleware(auth)

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
app.add_middleware(auth)

@app.get("/protected")
def protected():
    return {"message": "This route is protected"}

@app.get("/admin")
def admin():
    return {"message": "Admin route is protected"}
```

### Protecting FastAPI Documentation

You can protect your FastAPI's Swagger UI and ReDoc documentation by including their URLs in the protected routes:

```python
from fastapi import FastAPI
from fastapi_basic_auth import FastAPIBasicAuthMiddleware

app = FastAPI()

# Add middleware to protect docs
auth = FastAPIBasicAuthMiddleware(
    urls=[
        "/docs",           # Swagger UI
        "/redoc",         # ReDoc
        "/openapi.json",  # OpenAPI schema
        "/protected"      # Your protected routes
    ],
    users={"admin": "password"}
)
app.add_middleware(auth)

@app.get("/protected")
def protected():
    return {"message": "This route is protected"}

@app.get("/public")
def public():
    return {"message": "This route is public"}
```

This setup will:
- Require authentication to access Swagger UI at `/docs`
- Require authentication to access ReDoc at `/redoc`
- Protect the OpenAPI schema at `/openapi.json`
- Allow public access to non-protected routes
- Maintain the interactive features of Swagger UI after authentication

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
- FastAPI docs protection
  - Swagger UI (/docs)
  - ReDoc (/redoc)
  - OpenAPI schema (/openapi.json)