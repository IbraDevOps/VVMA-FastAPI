import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ISSUER = os.getenv("ISSUER")
AUDIENCE = os.getenv("AUDIENCE")

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import jwt
from app.models import users
import bcrypt

router = APIRouter()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Auth(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(auth: Auth):
    if auth.username not in users:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    stored_pw = users[auth.username]["password"]

    if not bcrypt.checkpw(auth.password.encode(), stored_pw.encode()):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    payload = {
        "sub": auth.username,
        "role": users[auth.username]["role"],
        "iss": ISSUER,
        "aud": AUDIENCE,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}
