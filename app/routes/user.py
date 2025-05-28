import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ISSUER = os.getenv("ISSUER")
AUDIENCE = os.getenv("AUDIENCE")

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from jose import jwt, JWTError
from app.models import users
import bcrypt

router = APIRouter()
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str
    password: str

# ----------------- Register -----------------
@router.post("/register")
def register(user: User):
    if user.username in users:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode('utf-8')
    users[user.username] = {"password": hashed_pw, "role": "user"}
    print(users)
    return {"message": f"User {user.username} registered"}

# ----------------- Token Decoding -----------------
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], audience=AUDIENCE, issuer=ISSUER)
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ----------------- Delete User -----------------
@router.delete("/delete-user/{username}")
def delete_user(username: str, token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    requester = payload.get("sub")
    role = payload.get("role")

    if username not in users:
        raise HTTPException(status_code=404, detail="User not found")

    if requester != username and role != "admin":
        raise HTTPException(status_code=403, detail="You are not allowed to delete this user")

    del users[username]
    return {"message": f"User {username} deleted"}

# ----------------- View Profile -----------------
@router.get("/profile/{username}")
def get_profile(username: str, token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    requester = payload.get("sub")
    role = payload.get("role")

    if username not in users:
        raise HTTPException(status_code=404, detail="User not found")

    if requester != username and role != "admin":
        raise HTTPException(status_code=403, detail="You are not allowed to view this profile")

    return {"profile": f"This is the profile of {username}"}

# ----------------- Update Profile -----------------
@router.patch("/update-profile/{username}")
def update_profile(username: str, update: dict, token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    requester = payload.get("sub")
    role = payload.get("role")

    if username not in users:
        raise HTTPException(status_code=404, detail="User not found")

    if requester != username and role != "admin":
        raise HTTPException(status_code=403, detail="You are not allowed to update this profile")

    if "role" in update:
        raise HTTPException(status_code=403, detail="You are not allowed to change roles")

    allowed_fields = {"password"}
    users[username].update({k: v for k, v in update.items() if k in allowed_fields})

    return {"message": f"User {username} updated", "new_data": users[username]}

# ----------------- Search (Safe Simulation) -----------------
@router.get("/search")
def search_users(query: str):
    blacklisted_keywords = ["'", "\"", "OR", "AND", "1=1", "--"]
    if any(keyword.lower() in query.lower() for keyword in blacklisted_keywords):
        raise HTTPException(status_code=400, detail="Invalid search query")

    results = [user for user in users if query.lower() in user.lower()]
    return {"results": results}
                                                                     
