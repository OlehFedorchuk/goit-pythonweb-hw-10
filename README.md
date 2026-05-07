📦 FastAPI Contacts API

REST API для управління контактами з JWT авторизацією, верифікацією email та завантаженням аватарів через Cloudinary.

⸻

🚀 Features

- 🔐 JWT Authentication (login/register)
- 📧 Email verification (Gmail SMTP)
- 👤 User profile (/users/me)
- 📇 Contacts CRUD API
- 🖼️ Avatar upload via Cloudinary
- 🐘 PostgreSQL database
- 🐳 Docker + Docker Compose
- 🌐 CORS enabled

⸻

🧱 Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- JWT (python-jose)
- Passlib (bcrypt)
- Cloudinary
- Docker

⸻

📁 Project Structure

.
├── Dockerfile
├── README.md
├── app
│ ├── auth.py
│ ├── auth_bearer.py
│ ├── cloudinary_service.py
│ ├── crud.py
│ ├── database.py
│ ├── email_service.py
│ ├── main.py
│ ├── models.py
│ ├── models_user.py
│ ├── routes
│ │ ├── auth.py
│ │ ├── contacts.py
│ │ └── users.py
│ ├── schemas.py
│ └── schemas_user.py
├── docker-compose.yml
└── pyproject.toml

⸻

⚙️ Environment Variables

Create .env file:

# DATABASE

POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=postgres
DATABASE_URL=postgresql://postgres:password@db:5432/postgres

# JWT

SECRET_KEY=your_super_secret_key
ALGORITHM=HS256

# MAIL (Gmail SMTP)

MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_google_app_password
MAIL_FROM=your_email@gmail.com
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587

# CLOUDINARY

CLOUDINARY_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
⸻

🐳 Run with Docker

Build and start

docker-compose up --build

Stop containers

docker-compose down

⸻

🔐 Authentication Flow

1. Register user

POST /auth/register

Sends verification email.

⸻

2. Verify email

Click link from email to activate account.

⸻

3. Login

POST /auth/login

Response:

{
"access_token": "jwt_token",
"token_type": "bearer"
}

⸻

👤 User Endpoints

Get current user

GET /users/me
Authorization: Bearer <token>

⸻

Upload avatar

PATCH /users/avatar

Uploads image to Cloudinary.

⸻

📇 Contacts API

- GET /contacts/ – list contacts
- POST /contacts/ – create contact
- GET /contacts/{id} – get contact
- PUT /contacts/{id} – update contact
- DELETE /contacts/{id} – delete contact

⸻

📧 Email Verification

Flow:

1. User registers
2. Email is sent via Gmail SMTP
3. User clicks verification link
4. Account becomes active

⸻

☁️ Cloudinary

Used for:

- Avatar uploads

⸻
