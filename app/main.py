from fastapi import FastAPI
from app.auth.router import router as auth_router
from app.auth.microsoft_router import router as microsoft_auth_router

app = FastAPI(
    title="NJMTech Mail OAuth API",
    description="An API for authenticating with Google and managing mail accounts.",
    version="0.1.0"
)

app.include_router(auth_router)
app.include_router(microsoft_auth_router)

@app.get("/")
async def root():
    return {"message": "API is running."}
