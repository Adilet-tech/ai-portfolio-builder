💼 AI Portfolio Builder (Foliomind)

A web application that allows users to create personal portfolio websites using artificial intelligence. The user inputs their skills, experience, and projects, and the AI automatically generates a professional portfolio: text, design, and page structure.

✨ Key Features

🔐 Secure Authentication: (✅ Done!) Registration and login using RS256 (asymmetric keys) and Argon2 (password hashing).

🤖 AI Content Generation: (✅ Done!) Automatic writing of "About Me", "Skills", and "Project Description" sections using the Google Gemini API.

🎨 Template Selection:

$$IN DEVELOPMENT$$

📥 Code Export:

$$IN DEVELOPMENT$$

🧩 Tech Stack

Frontend: React (Next.js)

Styling: TailwindCSS + shadcn/ui

Backend: FastAPI (Python)

Database: PostgreSQL + Alembic (migrations)

AI Integration: Google Gemini (gemini-pro)

Security: JWT (RS256) + Argon2

Containerization: Docker & Docker Compose

🚀 Getting Started (Local Setup)

To run the project locally using Docker:

1. Clone and Configure

Clone the repository:

git clone [https://github.com/Adilet-tech/ai-portfolio-builder.git](https://github.com/Adilet-tech/ai-portfolio-builder.git)
cd ai-portfolio-builder

Create a .env file:
In the project root (/), create a .env file. Copy the contents from .env.example and fill it with your data:

# Database Settings (PostgreSQL)

POSTGRES_USER=adikus
POSTGRES_PASSWORD=adikus
POSTGRES_DB=portfolio_db
DATABASE_URL=postgresql://adikus:adikus@db:5432/portfolio_db

# API Key from Google AI Studio

GOOGLE_API_KEY=AIzaSy... (YOUR KEY)
GOOGLE_MODEL_NAME=gemini-pro

# ... (and other settings from your .env) ...

Generate security keys (RS256):
Run these two commands in your terminal (in the project root) to create private_key.pem and public_key.pem:

openssl genrsa -out private_key.pem 2048
openssl rsa -in private_key.pem -pubout -out public_key.pem

Add the keys to .gitignore:
Make sure your .gitignore file includes a line to prevent uploading your private key:

\*.pem

2. Run Docker

Build and run the containers:
This command will build the images (frontend, backend) and run the containers (including the database).

docker compose up --build

Wait until all 3 services (db, backend, frontend) are running.

3. Database Setup (Alembic)

On the first run (or after docker compose down -v), the database will be empty. You must set it up.

Open a NEW terminal (without stopping docker compose up).

Create a migration (Alembic will compare models.py with the empty DB):

docker compose exec backend alembic revision --autogenerate -m "Create initial tables"

Apply the migration (This will create the users, portfolios, etc. tables):

docker compose exec backend alembic upgrade head

(Note: If you get the error NameError: name 'sqlmodel' is not defined, just add import sqlmodel to the top of the generated migration file in backend/alembic/versions/ and run upgrade again.)

4. Done!

Frontend is available at: http://localhost:3000

Backend (API) is available at: http://localhost:8000/docs

📁 Project Structure (Backend)

/backend
├── alembic/ # Alembic migration files
│ ├── versions/
│ └── env.py
├── app/
│ ├── api/ # API Routers
│ │ ├── auth.py # (Register, Login)
│ │ ├── users.py # (/users/me)
│ │ └── portfolio.py # (AI Generation)
│ ├── core/ # (Soon: Configs, Rate Limiter)
│ ├── services/
│ │ └── ai_service.py # (Google Gemini logic)
│ ├── db.py # DB connection setup
│ ├── dependencies.py # Endpoint protection (get_current_user)
│ ├── models.py # SQLModel models (tables)
│ ├── schemas.py # Pydantic schemas (DTOs)
│ ├── security.py # (Argon2, RS256 JWT)
│ └── main.py # Main FastAPI file
│
├── Dockerfile
└── requirements.txt

API Endpoints

Auth

POST /api/v1/auth/register - Register a new user.

POST /api/v1/auth/token - Get JWT token (login).

Users

GET /api/v1/users/me - (Protected) Get current user data.

Portfolio (AI Generation)

POST /api/v1/portfolio/generate/about - (Protected) Generate "About Me" section.

POST /api/v1/portfolio/generate/project - (Protected) Generate project description.

POST /api/v1/portfolio/generate/skills-structure - (Protected) Group skills.

POST /api/v1/portfolio/generate/full - (Protected) Generate full portfolio.

GET /api/v1/portfolio/me - (Protected) Get my portfolio from DB.

PUT /api/v1/portfolio/me/publish - (Protected) Publish portfolio.

GET /api/v1/portfolio/{portfolio_id}/public - (Public) Get portfolio by ID.
