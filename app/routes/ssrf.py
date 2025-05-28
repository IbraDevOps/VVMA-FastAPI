#Code for ssr vulnerbulty
# app/routes/ssrf.py

#from fastapi import APIRouter, HTTPException, Query
#import requests

#router = APIRouter()

#@router.get("/fetch-url")
#def fetch_url(target: str = Query(..., description="The URL to fetch")):
 #   try:
  #      response = requests.get(target, timeout=3)
   #     return {"status_code": response.status_code, "body": response.text[:200]}  # limit response
    #except requests.RequestException as e:
     #   raise HTTPException(status_code=500, detail=f"Failed to fetch URL: {str(e)}")

#Patching ssrf
from fastapi import APIRouter, HTTPException, Query
import requests
from urllib.parse import urlparse

router = APIRouter()

def is_private_ip(hostname):
    # Block localhost and metadata services
    return hostname.startswith("127.") or hostname.startswith("169.254.") or hostname == "localhost"

@router.get("/fetch-url")
def fetch_url(target: str = Query(...)):
    parsed_url = urlparse(target)

    if not parsed_url.scheme.startswith("http"):
        raise HTTPException(status_code=400, detail="Only HTTP/HTTPS URLs are allowed")

    if is_private_ip(parsed_url.hostname):
        raise HTTPException(status_code=403, detail="Access to internal IPs is blocked")

    try:
        response = requests.get(target, timeout=3)
        return {
            "status_code": response.status_code,
            "body": response.text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


