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

#SECRET_KEY = "supersecret"
ALGORITHM = "HS256"
#ISSUER = "vvma-fastapi"
#AUDIENCE = "vvma-users"
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

    # ✅ Hash the password
    hashed_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode('utf-8')

    # Storing the user details including hashed password and role
    users[user.username] = {"password": hashed_pw, "role": "user"}
    # Print users dictionary to verify
    print(users)  # This will show all users and their hashed passwords
    return {"message": f"User {user.username} registered"}


# Decode token
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], audience=AUDIENCE, issuer=ISSUER)
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

# View Profile (BOLA)
@router.get("/profile/{username}")
def get_profile(username: str, token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)

    # ❗ BOLA Vulnerability: No check if the token user == profile user
    if username not in users:
        raise HTTPException(status_code=404, detail="User not found")

    return {"profile": f"This is the profile of {username}"}

# Update Profile (Patched BOPLA)
@router.patch("/update-profile/{username}")
def update_profile(username: str, update: dict, token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)

    if username not in users:
        raise HTTPException(status_code=404, detail="User not found")

    # 🚫 Prevent changes to 'role' or other protected properties
    if "role" in update:
        raise HTTPException(status_code=403, detail="You are not allowed to update the role field")

    # ✅ Apply only allowed updates (e.g., password)
    allowed_fields = {"password"}
    users[username].update({k: v for k, v in update.items() if k in allowed_fields})

    return {"message": f"User {username} updated", "new_data": users[username]}

# Now we patch the SQL vuln code
@router.get("/search")
def search_users(query: str):
    # Simulated "safe" search
    blacklisted_keywords = ["'", "\"", "OR", "AND", "1=1", "--"]
    if any(keyword.lower() in query.lower() for keyword in blacklisted_keywords):
        raise HTTPException(status_code=400, detail="Invalid search query")

    results = [user for user in users if query.lower() in user.lower()]
    return {"results": results}

#print(users)  # This will print the users dictionary to verify password hashing
