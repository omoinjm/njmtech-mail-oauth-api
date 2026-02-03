import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.schema import UserMailAccount, OAuthToken
from app.repositories.base import BaseRepository
from app.auth.schemas import UserInfo, TokenData

class UserMailAccountRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_by_email(self, email: str) -> UserMailAccount | None:
        stmt = select(UserMailAccount).where(UserMailAccount.email_address_txt == email)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def create_or_update_user_with_token(self, user_info: UserInfo, token_data: TokenData, provider: str) -> UserMailAccount:
        user = await self.get_by_email(user_info.email)
        
        expires_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=token_data.expires_at)

        if user:
            # Update existing user's token
            if user.oauth_token:
                token = user.oauth_token[0]
                token.access_token_txt = token_data.access_token
                if token_data.refresh_token:
                    token.refresh_token_txt = token_data.refresh_token
                token.expires_at_utc = expires_at
            else:
                # Create a new token if one doesn't exist
                token = OAuthToken(
                    access_token_txt=token_data.access_token,
                    refresh_token_txt=token_data.refresh_token,
                    expires_at_utc=expires_at,
                    user_mail_account=user
                )
                self.session.add(token)
        else:
            # Create new user and token
            user = UserMailAccount(
                email_address_txt=user_info.email,
                provider_cd=provider,
                is_active_flg=True
            )
            token = OAuthToken(
                access_token_txt=token_data.access_token,
                refresh_token_txt=token_data.refresh_token,
                expires_at_utc=expires_at,
                user_mail_account=user
            )
            self.session.add(user)
            self.session.add(token)
            
        await self.session.commit()
        await self.session.refresh(user)
        return user
