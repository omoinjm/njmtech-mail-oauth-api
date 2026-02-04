import datetime
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.schema import UserMailAccount, OAuthToken
from app.repositories.base import BaseRepository
from app.auth.schemas import UserInfo, TokenData
from app.models.enums import Provider


class UserMailAccountRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_by_email(self, email: str) -> UserMailAccount | None:
        stmt = (
            select(UserMailAccount)
            .where(UserMailAccount.email_address_txt == email)
            .options(selectinload(UserMailAccount.oauth_token))
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def create_or_update_user_with_token(
        self, user_info: UserInfo, token_data: TokenData, provider: int
    ) -> UserMailAccount:
        user = await self.get_by_email(user_info.email)

        expires_at = (
            datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(seconds=token_data.expires_at)
        ).replace(tzinfo=None)

        if user:
            # Convert stored provider code to enum
            user_provider = Provider(user.provider_cd)
            req_provider = Provider(provider)

            # Ensure `provider` is also a Provider enum
            # (if it's coming in as a string or int, normalize it first)
            if user_provider.name != req_provider.name:
                raise ValueError(
                    f"Email '{user_info.email}' is already registered with provider "
                    f"'{user_provider.name}'. Cannot register with '{req_provider.name}'."
                )

            # Update existing user's token
            token = user.oauth_token

            if not token:
                raise RuntimeError("User exists but has no OAuth token")

            token.access_token_txt = token_data.access_token
            if token_data.refresh_token:
                token.refresh_token_txt = token_data.refresh_token
            token.expires_at_utc = expires_at

        else:
            # Create new user and token
            user = UserMailAccount(
                email_address_txt=user_info.email,
                provider_cd=provider,
                is_active_flg=True,
            )
            token = OAuthToken(
                access_token_txt=token_data.access_token,
                refresh_token_txt=token_data.refresh_token,
                expires_at_utc=expires_at,
                user_mail_account=user,
            )
            self.session.add(user)
            self.session.add(token)

        await self.session.commit()
        await self.session.refresh(user)
        return user
