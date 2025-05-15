from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# Simulated in-memory user store
users = {}

class User(BaseModel):
    username: str
    password: str  # ❗ No password strength validation (VULNERABILITY)

@router.post("/register")
def register(user: User):
    if user.username in users:
        raise HTTPException(status_code=400, detail="User already exists")
    
    users[user.username] = {"password": user.password}
    return {"message": f"User {user.username} registered"}
