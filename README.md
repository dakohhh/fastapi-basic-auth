# FastAPI Basic Auth

A simple and flexible Basic Authentication middleware for FastAPI applications.

## Installation

```bash
pip install fastapi-basic-auth
```

## Usage

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

## Features

- Protect specific routes with Basic Authentication
- Support for multiple users
- Flexible configuration
- Secure password comparison