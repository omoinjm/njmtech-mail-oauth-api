# Import necessary modules from FastAPI and Starlette.
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

# Import the authentication router and apilication settings.
from api.auth.router import router as auth_router
from api.core.config import settings

# Initialize the FastAPI apilication.
# Set the title, description, and version for API documentation (e.g., OpenAPI/Swagger UI).
app = FastAPI(
    title="NJMTech Mail OAuth API",
    description="An API for authenticating with Google and managing mail accounts.",
    version="0.1.0",
)

# Add SessionMiddleware to the apilication.
# This middleware is used for managing user sessions, essential for OAuth flows.
# The `secret_key` is used to sign the session cookies, ensuring their integrity.
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# Include the authentication router in the main apilication.
# This registers all the authentication-related endpoints (e.g., login, callback)
# defined in `api/auth/router.py` with the FastAPI apilication.
app.include_router(auth_router)


# Define a root endpoint for the API.
# This simple endpoint can be used to check if the API is running.
@app.get("/")
async def root():
    return {"message": "API is running."}

