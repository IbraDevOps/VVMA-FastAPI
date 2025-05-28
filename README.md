# VVMA-FastAPI

**Very Vulnerable Management API (FastAPI Edition)** is an intentionally vulnerable API written in Python using FastAPI. It is inspired by [VVMA](https://github.com/abigailajohn/VVMA), originally built in Node.js, and replicates the same OWASP Top 10 API vulnerabilities.

---

## 🔥 Features

### 👤 User Endpoints
- Create user
- Retrieve user details
- Update user
- Delete user

### 👥 Group Endpoints
- List all groups
- Retrieve group by ID
- Create a group (with invite code)
- Join group by ID or invite
- Refresh invite code
- Update/delete group (admin/owner only)
- Manage membership (remove/promote)

### 🔐 Password Reset
- Request password reset (OTP)
- Verify OTP and reset password

---

## 🐞 Vulnerabilities Demonstrated

- Weak Password Policy
- Broken Authentication
- BOLA
- BFLA
- Weak JWT Implementation
- BOPLA
- SQL Injection
- Weak Secret Key
- Email Enumeration
- SSRF
- Improper Inventory Management
- No Rate Limiting
- Plaintext Password Storage

---

## 🛠️ Setup

### Run Locally

```bash
git clone https://github.com/IbraDevOps/VVMA-FastAPI.git
cd VVMA-FastAPI
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 3000
<<<<<<< HEAD
=======

---

## ⚠️ Disclaimer

This API is **intentionally vulnerable** and is provided for **educational and testing purposes only**. Do **NOT** deploy this in production environments.

---

## 🙌 Credits

Inspired by the original [VVMA project](https://github.com/abigailajohn/VVMA) by [@abigailajohn](https://github.com/abigailajohn). Reimplemented in Python FastAPI by [@IbraDevOps](https://github.com/IbraDevOps).

