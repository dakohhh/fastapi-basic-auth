import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
import base64
from fastapi_basic_auth import FastAPIBasicAuthMiddleware


def test_protected_route():
    app = FastAPI()
    auth = FastAPIBasicAuthMiddleware(
        urls=["/protected"],
        users={"admin": "password"}
    )
    app.add_middleware(auth.build)
    
    @app.get("/protected")
    def protected():
        return {"message": "success"}
    
    @app.get("/public")
    def public():
        return {"message": "public"}
    
    client = TestClient(app)
    
    # Test unauthorized access
    response = client.get("/protected")
    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Basic"
    
    # Test authorized access
    credentials = base64.b64encode(b"admin:password").decode()
    headers = {"Authorization": f"Basic {credentials}"}
    response = client.get("/protected", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "success"}
    
    # Test invalid credentials
    wrong_credentials = base64.b64encode(b"admin:wrongpassword").decode()
    headers = {"Authorization": f"Basic {wrong_credentials}"}
    response = client.get("/protected", headers=headers)
    assert response.status_code == 401
    
    # Test malformed authorization header
    headers = {"Authorization": "Basic invalid_base64"}
    response = client.get("/protected", headers=headers)
    assert response.status_code == 401
    
    # Test non-Basic auth scheme
    headers = {"Authorization": "Bearer token"}
    response = client.get("/protected", headers=headers)
    assert response.status_code == 401
    
    # Test public route (should be accessible without auth)
    response = client.get("/public")
    assert response.status_code == 200
    assert response.json() == {"message": "public"}


def test_user_list_initialization():
    """Test initialization with list of BasicAuthUser objects"""
    from fastapi_basic_auth import BasicAuthUser
    
    app = FastAPI()
    auth = FastAPIBasicAuthMiddleware(
        urls=["/protected"],
        users=[BasicAuthUser(username="admin", password="password")]
    )
    app.add_middleware(auth.build)
    
    @app.get("/protected")
    def protected():
        return {"message": "success"}
    
    client = TestClient(app)
    
    credentials = base64.b64encode(b"admin:password").decode()
    headers = {"Authorization": f"Basic {credentials}"}
    response = client.get("/protected", headers=headers)
    assert response.status_code == 200