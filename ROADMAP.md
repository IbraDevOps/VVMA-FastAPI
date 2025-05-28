# 🛠️ VVMA-FastAPI Development Roadmap

This document outlines the step-by-step development and exploitation plan for the VVMA-FastAPI project — a deliberately vulnerable API built with FastAPI to simulate OWASP Top 10 API Security Risks.

---

##  Phase 1: User Module (Auth & Account Management)

| Step | Endpoint                          | Purpose                               | Vulnerability                         |
|------|-----------------------------------|---------------------------------------|----------------------------------------|
| 1    | `POST /api/register`             | User registration                     | Weak Password Policy                   |
| 2    | `POST /api/login`                | JWT-based login                       | Weak JWT Secret, Broken Authentication |
| 3    | `DELETE /api/delete-user/{username}` | Admin-only delete                 | BFLA (Broken Function Level Authorization) |
| 4    | `GET /api/profile/{username}`    | View any user’s profile               | BOLA (Broken Object Level Authorization) |
| 5    | `GET /api/admin`                 | Hidden admin dashboard                | Improper Inventory Management          |

---

##  Phase 2: Group Module (Access Control & Roles)

| Step | Endpoint                          | Purpose                               | Vulnerability                          |
|------|-----------------------------------|----------------------------------------|-----------------------------------------|
| 6    | `POST /api/groups`               | Create a group                         | No auth check                          |
| 7    | `GET /api/groups/{id}`           | View group by ID                       | BOLA                                   |
| 8    | `PATCH /api/groups/{id}`         | Update group details                   | BFLA                                   |
| 9    | `POST /api/groups/{id}/join`     | Join via invite code                   | No invite validation                   |
| 10   | `POST /api/groups/{id}/members/remove` | Manage members                  | BOPLA (Broken Object Property Level Auth) |

---

##  Phase 3: Password Reset Module (OTP & Enumeration)

| Step | Endpoint                          | Purpose                               | Vulnerability                          |
|------|-----------------------------------|----------------------------------------|-----------------------------------------|
| 11   | `POST /api/reset-password/request` | Request OTP via email               | Email Enumeration                      |
| 12   | `POST /api/reset-password/verify`  | Validate OTP                         | No Rate Limiting                       |
| 13   | `POST /api/reset-password/reset`   | Reset password                       | No token/session validation            |

---

##  Phase 4: System-Level Vulnerabilities

| Step | Endpoint                          | Purpose                               | Vulnerability                          |
|------|-----------------------------------|----------------------------------------|-----------------------------------------|
| 14   | User login (SQL lookup)           | Simulated raw SQL query                | SQL Injection                          |
| 15   | `POST /api/fetch-url`             | Test remote URL access                 | SSRF                                   |
| 16   | Password stored as plaintext      | No hashing or encryption               | Plaintext Password Storage             |

---

##  Goal

By the end of this roadmap, the project will:

- Replicate OWASP Top 10 API flaws
- Support both **attacking** and **patching** workflows
- Be dockerized and usable in CTF-style testing environments

---

> ✅ Track your commits with clear messages per step to make it easier for others (and yourself) to follow the logic.
