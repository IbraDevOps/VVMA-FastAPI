from fastapi import APIRouter
from app.models import users

router = APIRouter()

@router.post("/reset")
def reset_users():
    users.clear()
    return {"message": "All users deleted (reset done)"}
