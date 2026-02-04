from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.base import (
    BaseOAuth2,
    get_google_oauth_client,
    get_microsoft_oauth_client,
)
from app.auth.schemas import AuthResponse, TokenData, UserInfo
from app.core.database import get_db
from app.repositories.user_mail_account import UserMailAccountRepository
from app.models.enums import Provider

router = APIRouter(prefix="/auth", tags=["Authentication"])

PROVIDER_MAP = {
    "google": {
        "client": get_google_oauth_client,
        "provider_enum": Provider.GOOGLE,
    },
    "microsoft": {
        "client": get_microsoft_oauth_client,
        "provider_enum": Provider.MICROSOFT,
    },
}


@router.get("/{provider}/login")
async def login(provider: str, request: Request):
    if provider not in PROVIDER_MAP:
        raise HTTPException(status_code=404, detail="Provider not found")

    oauth_client: BaseOAuth2 = PROVIDER_MAP[provider]["client"]()
    login_url = oauth_client.get_login_url(request)
    return RedirectResponse(login_url)


@router.get("/{provider}/callback")
async def callback(
    provider: str,
    request: Request,
    code: str,
    state: str,
    db: AsyncSession = Depends(get_db),
) -> AuthResponse:
    if provider not in PROVIDER_MAP:
        raise HTTPException(status_code=404, detail="Provider not found")

    if "state" not in request.session or request.session["state"] != state:
        raise HTTPException(status_code=400, detail="Invalid state parameter")

    del request.session["state"]

    try:
        oauth_client: BaseOAuth2 = PROVIDER_MAP[provider]["client"]()
        token_payload = await oauth_client.exchange_code_for_tokens(code)

        access_token = token_payload.get("access_token")
        refresh_token = token_payload.get("refresh_token")
        expires_in = token_payload.get("expires_in")

        if not access_token or not expires_in:
            raise HTTPException(
                status_code=400, detail=f"Invalid token data from {provider}"
            )

        user_info_payload = await oauth_client.get_user_info(access_token)

        if provider == "google":
            email = user_info_payload.get("email")
        elif provider == "microsoft":
            email = user_info_payload.get("mail") or user_info_payload.get(
                "userPrincipalName"
            )

        if not email:
            raise HTTPException(
                status_code=400, detail=f"Could not retrieve user email from {provider}"
            )

        user_info = UserInfo(email=email)
        token_data = TokenData(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_in,
        )

        repo = UserMailAccountRepository(db)
        await repo.create_or_update_user_with_token(
            user_info, token_data, PROVIDER_MAP[provider]["provider_enum"]
        )

        return AuthResponse(user=user_info, token=token_data)

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred during {provider} OAuth callback: {e}",
        )

