# 🔍 Documented Vulnerabilities – VVMA FastAPI Edition

---

### 🔐 BOPLA – Broken Object Property Level Authorization

- **Status:** ✅ Patched  
- **Vulnerable Behavior:**  
  User could escalate privilege by modifying the `role` field directly:
  
  ```bash
  curl -X PATCH http://localhost:3000/api/update-profile/user1 \
    -H "Authorization: Bearer <user_token>" \
    -H "Content-Type: application/json" \
    -d '{"role": "admin"}'

Response before patch:

json
Copy
Edit
{
  "message": "User user1 updated",
  "new_data": {
    "password": "123456",
    "role": "admin"
  }
}

Patched Behavior:
Same request now returns:

json
Copy
Edit
{
  "detail": "You are not allowed to update the role field"
}

Patch Commit: e9791e0

yaml
Copy
Edit

---


 Patch Commit: e9791e0


### 🐞 SQL Injection (Simulated)

- **Status:** ❌ Vulnerable  
- **Vulnerable Endpoint:**  
  ```http
  GET /api/search?query=admin
curl "http://localhost:3000/api/search?query=admin%27%20OR%20%271%27=%271"

{
  "results": ["admin", "user1", "other records"]
}

Reason:
Input is directly processed without sanitization — vulnerable to SQL-like manipulation (or simulated logic injection in this case).

Patch Plan:

Add validation for query input

Reject suspicious patterns (like ' OR '1'='1)

Simulate use of parameterized search or proper filtering


SSRF – Server-Side Request Forgery

Vulnerable Endpoint:

http
Copy code
GET /api/fetch-url?target=http://<any-url>
Exploit Attempt:

bash
Copy code
curl "http://localhost:3000/api/fetch-url?target=http://127.0.0.1:3000/api/profile/admin"
Observed Behavior (Before Patch):

json
Copy code
{
  "status_code": 401,
  "body": "{\"detail\":\"Not authenticated\"}"
}

Patch plan: restric allowed urls to external domains only,block private IPs(like 127.0.0.1) use allow-lists and timeout limits on requests


No Rate Limiting on Login Endpoint
Status: ❌ Vulnerable

Vulnerable Endpoint:

http
Copy code
POST /api/login
Exploit Demonstration:
Simulated brute-force attack using a looped login request with wrong passwords:

bash
Copy code
for i in {1..10}; do
  curl -X POST http://localhost:3000/api/login \
    -H "Content-Type: application/json" \
    -d '{"username": "user1", "password": "wrongpass"}'
  echo -e "\nAttempt $i complete"
done
Observed Behavior:
All 10 requests returned:

json
Copy code
{
  "detail": "Invalid credentials"
}
Patching: add req throtlling,blocking or even delaying re after repeated failure,finally addning account CAPTCHA


User Registration with Hashed Password in FastAPI

Installed dependencies:

bash
Copy code
pip install fastapi uvicorn bcrypt
Created /register Endpoint:

Hash password using bcrypt and store it with the role user.

Code:

python
Copy code
@router.post("/register")
def register(user: User):
    if user.username in users:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode('utf-8')
    users[user.username] = {"password": hashed_pw, "role": "user"}
    print(users)  # Verify the user data
    return {"message": f"User {user.username} registered"}
Test Registration:

Used curl to test the endpoint:

bash
Copy code
curl -X POST http://127.0.0.1:3000/api/register \
-H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "securepassword123"}'
Verify:

Check print(users) in the server logs to confirm the password is hashed correctly.


### Weak JWT Secret / Token Tampering

- **Status:** Patched  
- **Issue:** Previously, the `SECRET_KEY` used to sign JWTs was hardcoded and weak (`"supersecret"`), allowing attackers to potentially forge or modify tokens.

- **Fix:**  
  - A strong secret is now generated using `secrets.token_hex(32)`.
  - It’s stored securely in a `.env` file and loaded using `dotenv`.
  - The app validates `iss`, `aud`, and `exp` claims properly.

- **Sample Secure JWT (decoded):**
  ```json
  {
    "sub": "Ibrahim",
    "role": "user",
    "iss": "vvma-fastapi",
    "aud": "vvma-users",
    "exp": 1748330751
  }
  ```

- **Patch Commit:** _<your-latest commit hash>_
