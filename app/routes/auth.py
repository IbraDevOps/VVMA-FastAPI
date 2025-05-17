from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import jwt
from app.models import users
router = APIRouter()

# Simulated users (replace with shared dict later)
#users = {
 #   "admin": {"password": "admin123", "role": "admin"},
  #  "user1": {"password": "123456", "role": "user"}
#    "user2": {"password": "12345678", "role": "user"}

#}

# ❗ Weak JWT setup (deliberately)
SECRET_KEY = "supersecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Auth(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(auth: Auth):
    if auth.username not in users or users[auth.username]["password"] != auth.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # ⚠️ Vulnerable JWT creation
    payload = {
        "sub": auth.username,
        "role": users[auth.username]["role"],
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}
