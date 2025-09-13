# 🧠 Mini-CRM AI – AI Note Summarizer Backend

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white) ![Python](https://img.shields.io/badge/Python_3.11-3776AB?style=for-the-badge&logo=python&logoColor=white) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) ![Celery](https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white)

A **REST API** providing **user authentication**, **multi-tenant note management**, and an **asynchronous background job** for summarizing note content. This project was built as part of a candidate backend assignment.

🚀 **Containerized with Docker** for easy setup and deployed to the cloud for quick access.

---

## 📚 Table of Contents
- [⚙️ Tech Stack](#️-tech-stack)
- [✨ Features](#-features)
- [🖥️ Local Setup](#️-local-setup)
- [🔑 Example Environment Variables](#-example-environment-variables)
- [📡 API Endpoints](#-api-endpoints)
- [☁️ Deployment](#️-deployment)
- [📜 License](#-license)

---

## ⚙️ Tech Stack

| Layer              | Technology |
|--------------------|------------|
| **Language**       | Python 3.11 |
| **Framework**      | FastAPI |
| **Database**       | PostgreSQL |
| **Async Tasks**    | Celery & Redis |
| **ORM**            | SQLAlchemy |
| **Migrations**     | Alembic |
| **AI Model**       | Hugging Face Transformers ([`sshleifer/distilbart-cnn-6-6`](https://huggingface.co/sshleifer/distilbart-cnn-6-6)) |
| **Containerization** | Docker & Docker Compose |

---

## ✨ Features

✅ **Authentication:** Secure email/password signup & login with JWTs.

✅ **Multi-Tenancy:** Role-based access (ADMIN, AGENT). Agents see only their own notes, Admins manage all.

✅ **Asynchronous Summarization:** Celery worker handles summarization in the background — API stays responsive.

✅ **Job Status Tracking:** Check summarization status (`queued`, `processing`, `done`, `failed`).

✅ **Local AI Model:** Self-contained Hugging Face model — no API keys required.

✅ **Containerized Setup:** Single `docker-compose up` to launch the whole stack.

---

## 🖥️ Local Setup

You’ll need **Docker** and **Docker Compose** installed.

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Balghi/mini-crm-ai.git
cd mini-crm-ai
```

### 2️⃣ Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Default values are pre-configured for local use.

### 3️⃣ Build & Run with Docker Compose
```bash
docker-compose up --build
```
Run in detached mode:
```bash
docker-compose up --build -d
```

### 4️⃣ Apply Database Migrations
After containers are running:
```bash
docker-compose exec api alembic upgrade head
```

Your API is now live at **http://localhost:8000** 🎉

---

## 🔑 Example Environment Variables

Create a `.env` file using the template below:

```env
# URL for local Postgres database inside Docker
DATABASE_URL="postgresql://user:password@db:5432/notesdb"

# URL for local Redis broker inside Docker
CELERY_BROKER_URL="redis://redis:6379/0"

# Secret key for signing JWTs - CHANGE FOR PRODUCTION
SECRET_KEY="a_very_secret_key_that_should_be_long_and_random"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 📡 API Endpoints

Interactive **Swagger Docs** available at **http://localhost:8000/docs**.

| Method | Endpoint | Description |
|--------|----------|-------------|
| **POST** | `/api/v1/signup` | Create a new user (defaults to `AGENT` role). |
| **POST** | `/api/v1/login` | Get a JWT token. |
| **POST** | `/api/v1/notes` | Create a new note (queues summarization job). |
| **GET** | `/api/v1/notes/{id}` | Fetch note & check summarization status. |

---

## ☁️ Deployment

The API is deployed on **Koyeb**:  
🔗 **Live URL:** [standard-kelcy-balghi-9b55f2cb.koyeb.app](https://standard-kelcy-balghi-9b55f2cb.koyeb.app/)

> ⚠️ **Note:** On the free tier, background summarization is disabled (due to memory limits). All **Auth, Tenancy, and CRUD** features work as expected.
> Run locally via Docker to experience full functionality with async AI summarization.

---

## 📜 License

This project is provided as part of a candidate assignment and is open for review and educational purposes.

---

💡 **Tip:** If you find this useful or want to test the full async AI-powered version, clone and run it locally!

---

**Made with ❤️ using FastAPI & Hugging Face**

