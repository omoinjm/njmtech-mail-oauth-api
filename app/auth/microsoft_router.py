from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.microsoft import MicrosoftOAuth2
from app.auth.schemas import AuthResponse, TokenData, UserInfo
from app.core.database import get_db
from app.repositories.user_mail_account import UserMailAccountRepository

router = APIRouter(prefix="/auth/microsoft", tags=["Authentication"])

@router.get("/login")
async def login_to_microsoft():
    login_url = MicrosoftOAuth2.get_login_url()
    return RedirectResponse(login_url)

@router.get("/callback")
async def microsoft_callback(code: str, db: AsyncSession = Depends(get_db)) -> AuthResponse:
    try:
        # Exchange code for tokens
        token_payload = await MicrosoftOAuth2.exchange_code_for_tokens(code)
        
        # Extract token data
        access_token = token_payload.get("access_token")
        refresh_token = token_payload.get("refresh_token")
        expires_in = token_payload.get("expires_in") # Microsoft returns 'expires_in' in seconds

        if not access_token or not expires_in:
            raise HTTPException(status_code=400, detail="Invalid token data from Microsoft")

        # Get user info from Microsoft Graph API
        user_info_payload = await MicrosoftOAuth2.get_user_info(access_token)
        email = user_info_payload.get("mail") or user_info_payload.get("userPrincipalName")

        if not email:
            raise HTTPException(status_code=400, detail="Could not retrieve user email from Microsoft")

        # Prepare data for repository
        user_info = UserInfo(email=email)
        token_data = TokenData(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_in
        )

        # Use repository to save data
        repo = UserMailAccountRepository(db)
        await repo.create_or_update_user_with_token(user_info, token_data, "microsoft")

        # Return a response
        return AuthResponse(user=user_info, token=token_data)

    except HTTPException as e:
        raise e
    except Exception as e:
        # Log the exception for debugging
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred during Microsoft OAuth callback.")
