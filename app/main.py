from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.auth.router import router as auth_router
from app.core.config import settings

app = FastAPI(
    title="NJMTech Mail OAuth API",
    description="An API for authenticating with Google and managing mail accounts.",
    version="0.1.0"
)

# Add SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "API is running."}
