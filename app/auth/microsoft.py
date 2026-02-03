import httpx
from app.core.config import settings

MICROSOFT_AUTHORIZATION_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
MICROSOFT_TOKEN_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
MICROSOFT_USERINFO_URL = "https://graph.microsoft.com/v1.0/me"

SCOPES = [
    "openid",
    "offline_access",
    "User.Read",
    "Mail.Read",
    "Mail.Send"
]

class MicrosoftOAuth2:
    @staticmethod
    def get_login_url() -> str:
        params = {
            "client_id": settings.MICROSOFT_CLIENT_ID,
            "redirect_uri": settings.MICROSOFT_REDIRECT_URI,
            "response_type": "code",
            "scope": " ".join(SCOPES),
            "access_type": "offline", # This might not be directly applicable for MS but is a common OAuth param
            "prompt": "consent",
        }
        # Microsoft uses the 'state' parameter, but for a basic flow, it's optional if not handling CSRF
        # For production, a 'state' parameter should be generated and validated.
        return f"{MICROSOFT_AUTHORIZATION_URL}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"

    @staticmethod
    async def exchange_code_for_tokens(code: str) -> dict:
        async with httpx.AsyncClient() as client:
            payload = {
                "client_id": settings.MICROSOFT_CLIENT_ID,
                "scope": " ".join(SCOPES),
                "code": code,
                "redirect_uri": settings.MICROSOFT_REDIRECT_URI,
                "grant_type": "authorization_code",
                "client_secret": settings.MICROSOFT_CLIENT_SECRET,
            }
            response = await client.post(MICROSOFT_TOKEN_URL, data=payload)
            response.raise_for_status()
            return response.json()

    @staticmethod
    async def get_user_info(access_token: str) -> dict:
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {access_token}"}
            response = await client.get(MICROSOFT_USERINFO_URL, headers=headers)
            response.raise_for_status()
            return response.json()
