from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.models import users
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ISSUER = os.getenv("ISSUER")
AUDIENCE = os.getenv("AUDIENCE")

def decode_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            issuer=ISSUER,
            audience=AUDIENCE
        )
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/reset")
def reset_users(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)

    if payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Only admins can perform reset")

    users.clear()
    return {"message": "All users deleted (reset done)"}
