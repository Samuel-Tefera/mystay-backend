# mystay-backend

`mystay-backend` is the backend service for the **MyStay** application, built using **FastAPI**.
It handles authentication, database operations, email services, and provides RESTful APIs consumed by the frontend.

The project is designed to be simple, fast, and easy to set up for local development.

---

## Tech Stack

- FastAPI
- Python 3.10+
- Uvicorn
- SQLAlchemy
- Google OAuth
- SMTP Email Service

---

## Frontend Repository

The frontend for this project lives in a separate repository:

https://github.com/KirubelWondwossen/mystay-frontend

---

## Getting Started

Follow the steps below to run the backend locally.

---

## Prerequisites

- Python 3.10 or higher
- pip
- Virtual environment support (`venv`)

---

## Environment Variables

Create a `.env` file in the project root and add the following variables:

```env
DATABASE_URL=your_database_connection_string

GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=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
GOOGLE_REDIRECT_URI=your_google_redirect_uri

EMAIL_ADDRESS=your_email_address
EMAIL_APP_PASSWORD=your_email_app_password

FRONTEND_RESET_PASSWORD_URL=your_frontend_reset_password_url
```

## How to Run the Application

### 1. Create a Virtual Environment

From the project root:
```bash
python -m venv venv
```
Activate the virtual environment:
windows
```bash
venv\Scripts\activate
```
macOS / Linux
```bash
source venv/bin/activate
```

### 2. Install Dependencies

Install all required packages from requirements.txt:
```bash
pip install -r requirements.txt
```

### 3. Run the Server

Start the FastAPI application using Uvicorn:
```bash
uvicorn app.main:app --reload
```

### 4. Access the API

API Base URL: http://127.0.0.1:8000

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc
