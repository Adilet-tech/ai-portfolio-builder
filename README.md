# 💼 AI Portfolio Builder (Foliomind)

[![License: MIT](https://img.shields.io/badge/License-MIT-green)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0-lightgrey)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2.0-blue?logo=react)](https://reactjs.org/)
[![Docker](https://img.shields.io/badge/Docker-24.0.6-blue?logo=docker)](https://www.docker.com/)

A web application that allows users to create personal portfolio websites using artificial intelligence. Users input their skills, experience, and projects, and the AI automatically generates professional portfolio content, design, and page structure.

---

## ✨ Key Features

- **🔐 Secure Authentication** ✅  
  Registration and login using RS256 (asymmetric keys) and Argon2 (password hashing). Supports Refresh Tokens.

- **🤖 AI Content Generation** ✅  
  Automatic writing of "About Me", "Skills", and "Project Description" sections using Google Gemini API.

- **🗃️ Database & Migrations** ✅  
  PostgreSQL configured with Alembic for schema migrations.

- **🛡️ API Protection** ✅  
  Protected routes with `get_current_user` dependencies and a Rate Limiter to prevent API abuse.

- **🎨 Template Selection** (In Development)

- **📥 Code Export** (In Development)

---

## 🧩 Tech Stack

- **Frontend:** React (Next.js)
- **Styling:** TailwindCSS + shadcn/ui
- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL + Alembic
- **AI Integration:** Google Gemini (models/gemini-2.5-flash)
- **Security:** JWT (RS256) + Argon2
- **Containerization:** Docker & Docker Compose

---

## 🚀 Getting Started (Local Setup)

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Adilet-tech/ai-portfolio-builder.git
cd ai-portfolio-builder
2️⃣ Configure Environment Variables
Create a .env file in the project root based on .env.example:
# Database Settings
POSTGRES_USER=adikus
POSTGRES_PASSWORD=adikus
POSTGRES_DB=portfolio_db
DATABASE_URL=postgresql://adikus:adikus@db:5432/portfolio_db

# Google Gemini API
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
GOOGLE_MODEL_NAME=models/gemini-2.5-flash

# Token Lifespan
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# App Settings
ENVIRONMENT=development
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
LOG_LEVEL=DEBUG
3️⃣ Generate Security Keys (RS256)
openssl genrsa -out private_key.pem 2048
openssl rsa -in private_key.pem -pubout -out public_key.pem
Add *.pem to .gitignore to avoid uploading private keys.
4️⃣ Run Docker
docker compose up --build
Wait for all services (db, backend, frontend) to be running.
5️⃣ Setup the Database (Alembic)
Open a new terminal (while Docker is running):
# Generate migration
docker compose exec backend alembic revision --autogenerate -m "Create all tables"

# Apply migration
docker compose exec backend alembic upgrade head
⚠️ If you get NameError: name 'sqlmodel' is not defined, add import sqlmodel at the top of the new migration file and rerun the upgrade.
6️⃣ Access the Application
Frontend: http://localhost:3000
Backend (API Docs): http://localhost:8000/docs
📁 Project Structure (Backend)
/backend
├── alembic/
│   ├── versions/
│   └── env.py
├── app/
│   ├── api/
│   │   ├── auth.py
│   │   ├── users.py
│   │   └── portfolio.py
│   ├── core/
│   │   └── rate_limiter.py
│   ├── services/
│   │   └── ai_service.py
│   ├── db.py
│   ├── dependencies.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   └── main.py
├── Dockerfile
└── requirements.txt
🗺️ API Endpoints
Auth
POST /api/v1/auth/register - Register a new user.
POST /api/v1/auth/token - Get JWT token (login).
Users
GET /api/v1/users/me - (Protected) Get current user's data.
Portfolio (AI Generation)
POST /api/v1/portfolio/generate/about - (Protected) Generate "About Me".
POST /api/v1/portfolio/generate/project - (Protected) Generate project description.
POST /api/v1/portfolio/generate/skills-structure - (Protected) Group skills into categories.
POST /api/v1/portfolio/generate/full - (Protected) Generate a full portfolio.
GET /api/v1/portfolio/me - (Protected) Get current portfolio.
PUT /api/v1/portfolio/me/publish - (Protected) Publish portfolio.
GET /api/v1/portfolio/{portfolio_id}/public - (Public) Get published portfolio by ID.
💾 Git Push Instructions
# Stop Docker
Ctrl + C

# Commit changes
git add .
git commit -m "feat(backend): Complete backend infrastructure, auth, and Gemini AI endpoints"

# Push to GitHub
git push origin main
```
