from abc import ABC, abstractmethod
import secrets
import httpx
from api.core.config import settings


class BaseOAuth2(ABC):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        authorization_url: str,
        token_url: str,
        userinfo_url: str,
        scopes: list[str],
        provider: str,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.authorization_url = authorization_url
        self.token_url = token_url
        self.userinfo_url = userinfo_url
        self.scopes = scopes
        self.provider = provider

    def get_login_url(self, request) -> str:
        state = secrets.token_hex(16)
        request.session["state"] = state

        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": " ".join(self.scopes),
            "state": state,
        }

        if self.provider == "google":
            params.update(
                {
                    "access_type": "offline",
                    "prompt": "consent",
                }
            )
        elif self.provider == "microsoft":
            params.update({"prompt": "consent"})

        return f"{self.authorization_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"

    async def exchange_code_for_tokens(self, code: str) -> dict:
        async with httpx.AsyncClient() as client:
            payload = {
                "code": code,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "redirect_uri": self.redirect_uri,
                "grant_type": "authorization_code",
            }
            if self.provider == "microsoft":
                payload["scope"] = " ".join(self.scopes)

            response = await client.post(self.token_url, data=payload)
            response.raise_for_status()
            return response.json()

    async def get_user_info(self, access_token: str) -> dict:
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {access_token}"}
            response = await client.get(self.userinfo_url, headers=headers)
            response.raise_for_status()
            return response.json()


def get_google_oauth_client() -> BaseOAuth2:
    return BaseOAuth2(
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        redirect_uri=settings.GOOGLE_REDIRECT_URI,
        authorization_url="https://accounts.google.com/o/oauth2/v2/auth",
        token_url="https://oauth2.googleapis.com/token",
        userinfo_url="https://www.googleapis.com/oauth2/v1/userinfo",
        scopes=[
            "openid",
            "email",
            "profile",
            "https://www.googleapis.com/auth/gmail.readonly",
            "https://www.googleapis.com/auth/gmail.send",
        ],
        provider="google",
    )


def get_microsoft_oauth_client() -> BaseOAuth2:
    return BaseOAuth2(
        client_id=settings.MICROSOFT_CLIENT_ID,
        client_secret=settings.MICROSOFT_CLIENT_SECRET,
        redirect_uri=settings.MICROSOFT_REDIRECT_URI,
        authorization_url="https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
        token_url="https://login.microsoftonline.com/common/oauth2/v2.0/token",
        userinfo_url="https://graph.microsoft.com/v1.0/me",
        scopes=["openid", "offline_access", "User.Read", "Mail.Read", "Mail.Send"],
        provider="microsoft",
    )
