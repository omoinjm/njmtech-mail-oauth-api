# Google OAuth (Gmail) with FastAPI + PostgreSQL

This document is a **prompt to provide to Gemini**.  
It instructs Gemini to generate a **production-ready backend** using **Python, FastAPI, Google OAuth 2.0, and PostgreSQL**.

---

## 🎯 Objective

Build a **FastAPI backend** that authenticates users with **Google OAuth 2.0**, requests Gmail permissions, and stores OAuth tokens and email account metadata in a **PostgreSQL database**.

The API must:

- Authenticate with Google
- Request Gmail read & send permissions
- Store OAuth tokens securely
- Persist user email accounts
- Use environment variables for all secrets

---

## 🧱 Tech Stack & Requirements

- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Authentication**: Google OAuth 2.0 (Authorization Code Flow)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy 2.0 (async)
- **Migrations**: Alembic
- **HTTP Client**: httpx
- **Environment Management**: python-dotenv
- **Data Validation**: Pydantic v2
- **API Style**: REST
- **Security**:
  - No secrets committed to source control
  - All sensitive values in `.env`
  - OAuth tokens stored securely

---

## 🔐 Google OAuth Configuration

### Required Scopes

```
openid
email
profile
https://www.googleapis.com/auth/gmail.readonly
https://www.googleapis.com/auth/gmail.send
```

---

## 🌐 API Endpoints

### GET /auth/google/login

Redirects user to Google OAuth consent screen

### GET /auth/google/callback

Handles OAuth callback, exchanges tokens, saves user and token data

---

## 🗄️ Database Schema

### user_mail_accounts

```
user_mail_account_id
email_address_txt
provider_cd
is_active_flg
created_at_utc
modified_at_utc
```

### oauth_tokens

```
oauth_token_id
user_mail_account_id
access_token_txt
refresh_token_txt
expires_at_utc
created_at_utc
modified_at_utc
```

---

## 📁 Project Structure

```
app/
├── main.py
├── core/
├── auth/
├── models/
├── repositories/
└── migrations/
```

---

## ⚙️ Environment Variables (.env)

```
DATABASE_URL=
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=
```

---

## 📘 Final Deliverable

Gemini must generate a complete FastAPI OAuth backend ready for production.
