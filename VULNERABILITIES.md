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
