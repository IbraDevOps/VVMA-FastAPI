#Code for ssr vulnerbulty
# app/routes/ssrf.py

from fastapi import APIRouter, HTTPException, Query
import requests

router = APIRouter()

@router.get("/fetch-url")
def fetch_url(target: str = Query(..., description="The URL to fetch")):
    try:
        response = requests.get(target, timeout=3)
        return {"status_code": response.status_code, "body": response.text[:200]}  # limit response
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch URL: {str(e)}")



