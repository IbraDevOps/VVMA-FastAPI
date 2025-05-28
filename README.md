
````markdown
# VVMA-FastAPI

**Very Vulnerable Management API (FastAPI Edition)** is an intentionally vulnerable API written in Python using FastAPI. It is inspired by [VVMA](https://github.com/abigailajohn/VVMA), originally built in Node.js, and replicates the same OWASP Top 10 API vulnerabilities.

---

##  Features

###  User Endpoints
- Create user
- Retrieve user details
- Update user
- Delete user

###  Group Endpoints _(Planned — Not Implemented)_
> These endpoints were originally scoped for the project but not implemented, as the primary focus was on demonstrating and remediating OWASP Top 10 API vulnerabilities.
- List all groups
- Retrieve group by ID
- Create a group (with invite code)
- Join group by ID or invite
- Refresh invite code
- Update/delete group (admin/owner only)
- Manage membership (remove/promote)

### 🔐 Password Reset
- Request password reset (via masked message)
- Verify OTP and reset password

---

## 🐞 Vulnerabilities Demonstrated & Patched

The following OWASP Top 10 API vulnerabilities were **intentionally introduced, exploited, and patched**:

- ✅ Weak Password Policy
- ✅ Broken Authentication
- ✅ Broken Object Level Authorization (BOLA)
- ✅ Broken Function Level Authorization (BFLA)
- ✅ Weak JWT Implementation
- ✅ Broken Object Property Level Authorization (BOPLA)
- ✅ SQL Injection
- ✅ Weak Secret Key
- ✅ Email Enumeration
- ✅ Server-Side Request Forgery (SSRF)
- ✅ Improper Inventory Management
- ✅ No Rate Limiting
- ✅ Plaintext Password Storage

---

## 🛠 Setup

### Run Locally

```bash
git clone https://github.com/IbraDevOps/VVMA-FastAPI.git
cd VVMA-FastAPI
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 3000
````

---

## ⚠ Disclaimer

This API is **intentionally vulnerable** and is provided for **educational and testing purposes only**. Do **NOT** deploy this in production environments.

---

## 🙌 Credits

Inspired by the original [VVMA project](https://github.com/abigailajohn/VVMA) by [@abigailajohn](https://github.com/abigailajohn).
Reimplemented in Python FastAPI by [@IbraDevOps](https://github.com/IbraDevOps).

```


