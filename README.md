# FastAPI Google & Microsoft OAuth Backend

This project is a production-ready backend built with Python, FastAPI, Google OAuth 2.0, Microsoft OAuth 2.0, and PostgreSQL. It authenticates users with Google or Microsoft, requests Gmail/Outlook permissions, and stores OAuth tokens and email account metadata.

## Prerequisites

- Python 3.11+
- Pip
- A running PostgreSQL database instance

## Setup Instructions

1.  **Create a Virtual Environment:**
    It's highly recommended to use a virtual environment to manage project dependencies.

    ```bash
    python -m venv venv
    source venv/bin/activate
    # On Windows, use `venv\Scripts\activate`
    ```

2.  **Install Dependencies:**
    Install all the required Python packages.

    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables:**
    Create a `.env` file from the example and fill in your details.

    ```bash
    cp .env.example .env
    ```

    You will need to edit the `.env` file with your specific credentials for both Google and Microsoft:
    - `DATABASE_URL`: Your asynchronous PostgreSQL connection string (e.g., `postgresql+asyncpg://user:password@localhost/dbname`).

    ### Google OAuth Configuration
    - `GOOGLE_CLIENT_ID`: Your Google Cloud project's OAuth Client ID.
    - `GOOGLE_CLIENT_SECRET`: Your Google Cloud project's Client Secret.
    - `GOOGLE_REDIRECT_URI`: The callback URL. For local development, this is typically `http://localhost:8000/auth/google/callback`. **This must match exactly** with the one configured in your Google Cloud OAuth consent screen settings.

    ### Microsoft OAuth Configuration
    - `MICROSOFT_CLIENT_ID`: Your Azure AD application's Client ID.
    - `MICROSOFT_CLIENT_SECRET`: Your Azure AD application's Client Secret.
    - `MICROSOFT_REDIRECT_URI`: The callback URL. For local development, this is typically `http://localhost:8000/auth/microsoft/callback`. **This must match exactly** with the one configured in your Azure AD application's redirect URIs.

## Database Migrations

This project uses Alembic to manage database schema changes.

**Important Note:** If your PostgreSQL database already contains the `user_mail_accounts` and `oauth_tokens` tables with the expected schema, you can skip applying migrations. These steps are primarily for initializing a new database or applying schema changes.

1.  **Generate the Initial Migration (if not already done):**
    If this is the first time setting up the database, with your environment configured, Alembic can now compare the models defined in `app/models` to your database and generate the first migration script.

    ```bash
    alembic revision --autogenerate -m "Initial migration"
    ```
    This will create a new file in the `migrations/versions/` directory.

2.  **Apply the Migration:**
    Run the migration script to create the `user_mail_accounts` and `oauth_tokens` tables in your database.

    ```bash
    alembic upgrade head
    ```

## Running the Application

To start the FastAPI server, use `uvicorn`.

```bash
uvicorn app.main:app --reload
```

The `--reload` flag enables hot-reloading, which is useful for development. The server will be available at `http://localhost:8000`.

## How to Use

### Google OAuth

1.  **Start the Authentication Flow:**
    Open your web browser and navigate to:
    [http://localhost:8000/auth/google/login](http://localhost:8000/auth/google/login)

2.  **Google Consent Screen:**
    You will be redirected to Google to authenticate and grant the requested permissions (for Gmail read/send, profile, and email).

3.  **Callback and Token Storage:**
    After you approve, Google will redirect you back to the application at the `/auth/google/callback` endpoint. The backend will exchange the authorization code for an access token and refresh token, retrieve your email address, and save the account and token information to the PostgreSQL database.

4.  **API Response:**
    Your browser will display a JSON response containing your user information and the tokens received from Google.

### Microsoft OAuth

1.  **Start the Authentication Flow:**
    Open your web browser and navigate to:
    [http://localhost:8000/auth/microsoft/login](http://localhost:8000/auth/microsoft/login)

2.  **Microsoft Consent Screen:**
    You will be redirected to Microsoft to authenticate and grant the requested permissions (for Outlook Mail read/send, profile, and email).

3.  **Callback and Token Storage:**
    After you approve, Microsoft will redirect you back to the application at the `/auth/microsoft/callback` endpoint. The backend will exchange the authorization code for an access token and refresh token, retrieve your email address, and save the account and token information to the PostgreSQL database.

4.  **API Response:**
    Your browser will display a JSON response containing your user information and the tokens received from Microsoft.