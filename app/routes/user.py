from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from jose import jwt, JWTError
from app.models import users

router = APIRouter()

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Model
class User(BaseModel):
    username: str
    password: str

# Register Endpoint
@router.post("/register")
def register(user: User):
    if user.username in users:
        raise HTTPException(status_code=400, detail="User already exists")
    
    users[user.username] = {"password": user.password, "role": "user"}  # Add default role
    return {"message": f"User {user.username} registered"}

# Decode token
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Delete User (BFLA)
@router.delete("/delete-user/{username}")
def delete_user(username: str, token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)

    if username not in users:
        raise HTTPException(status_code=404, detail="User not found")

    del users[username]
    return {"message": f"User {username} deleted"}


@router.get("/profile/{username}")
def get_profile(username: str, token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)

    # ❗ BOLA Vulnerability: No check if the token user == profile user
    if username not in users:
        raise HTTPException(status_code=404, detail="User not found")

    return {"profile": f"This is the profile of {username}"}
