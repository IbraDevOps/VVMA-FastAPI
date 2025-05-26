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
