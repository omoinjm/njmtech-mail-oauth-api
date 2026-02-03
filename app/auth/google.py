import httpx
from app.core.config import settings

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"

SCOPES = [
    "openid",
    "email",
    "profile",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
]

class GoogleOAuth2:
    @staticmethod
    def get_login_url() -> str:
        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "scope": " ".join(SCOPES),
            "access_type": "offline",
            "prompt": "consent",
        }
        return f"{GOOGLE_AUTH_URL}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"

    @staticmethod
    async def exchange_code_for_tokens(code: str) -> dict:
        async with httpx.AsyncClient() as client:
            payload = {
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            }
            response = await client.post(GOOGLE_TOKEN_URL, data=payload)
            response.raise_for_status()
            return response.json()

    @staticmethod
async def get_user_info(access_token: str) -> dict:
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {access_token}"}
            response = await client.get(GOOGLE_USERINFO_URL, headers=headers)
            response.raise_for_status()
            return response.json()
