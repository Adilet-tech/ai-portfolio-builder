## 💼 AI Portfolio Builder (Foliomind)

[![License: MIT](https://img.shields.io/badge/License-MIT-green)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0-lightgrey)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2.0-blue?logo=react)](https://reactjs.org/)
[![Docker](https://img.shields.io/badge/Docker-24.0.6-blue?logo=docker)](https://www.docker.com/)

A full-stack web application designed to empower users to create professional personal portfolio websites using **Artificial Intelligence**. Users input their core skills, experience, and projects, and the AI automatically generates structured content, design recommendations, and page architecture.

---

## ✨ Key Features

* **🔐 Secure Authentication** ✅
    * Robust registration and login implemented with **RS256** (asymmetric keys) and **Argon2** (password hashing). Includes support for Refresh Tokens.
* **🤖 AI Content Generation** ✅
    * Automatic drafting of "About Me," "Skills," and "Project Description" sections using the **Google Gemini API**.
* **🗃️ Database & Migrations** ✅
    * **PostgreSQL** configured with **Alembic** for reliable schema migration management.
* **🛡️ API Protection** ✅
    * Protected API routes secured via `get_current_user` dependencies and an integrated **Rate Limiter** to prevent abuse.
* **🎨 Template Selection** (In Development)
* **📥 Code Export** (In Development)

---

## 🧩 Tech Stack

| Component | Technologies |
| :--- | :--- |
| **Backend** | **FastAPI** (Python) |
| **Frontend** | **React** (Next.js) |
| **Styling** | **TailwindCSS** + shadcn/ui |
| **Database** | **PostgreSQL** + Alembic |
| **AI Integration** | **Google Gemini** (`models/gemini-2.5-flash`) |
| **Security** | **JWT (RS256)** + Argon2 |
| **Containerization** | **Docker** & Docker Compose |

---

## 🚀 Getting Started (Local Setup)

### 1️⃣ Clone the Repository

# Clone the repository from GitHub
git clone [https://github.com/Adilet-tech/ai-portfolio-builder.git](https://github.com/Adilet-tech/ai-portfolio-builder.git)

# Navigate into the project directory
cd ai-portfolio-builder
2️⃣ Configure Environment Variables
Action: Create a .env file in the project root based on the provided .env.example:

# Example content for the .env file:

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
Action: Generate keys for JWT authentication.

# Generate a 2048-bit RSA private key
openssl genrsa -out private_key.pem 2048

# Extract the public key from the private key
openssl rsa -in private_key.pem -pubout -out public_key.pem

# Note: Add *.pem to your .gitignore file to prevent committing private keys.

4️⃣ Run Docker Containers
Action: Build images and start all services (db, backend, frontend).

docker compose up --build

5️⃣ Set Up the Database (Alembic Migrations)
Action: Open a new terminal (while Docker is running) and run the following commands to initialize the database schema.

# 1. Generate the initial migration file

docker compose exec backend alembic revision --autogen -m "Create all tables"

# 2. Apply the migration to the database
docker compose exec backend alembic upgrade head

# ⚠️ Troubleshooting: If you get NameError: name 'sqlmodel' is not defined, 
# manually add 'import sqlmodel' at the top of the new migration file
# and rerun the 'alembic upgrade head' command.

6️⃣ Access the Application
Result: Application services are running and accessible.

# Frontend (Client App)
http://localhost:3000

# Backend (API Documentation - Swagger/OpenAPI)
http://localhost:8000/docs


git push origin main


git push origin main
