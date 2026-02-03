import datetime
from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    ForeignKey,
    func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class UserMailAccount(Base):
    __tablename__ = 'user_mail_accounts'

    user_mail_account_id: Mapped[int] = mapped_column(primary_key=True)
    email_address_txt: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    provider_cd: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active_flg: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at_utc: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    modified_at_utc: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    oauth_token: Mapped["OAuthToken"] = relationship(back_populates="user_mail_account")

class OAuthToken(Base):
    __tablename__ = 'oauth_tokens'

    oauth_token_id: Mapped[int] = mapped_column(primary_key=True)
    user_mail_account_id: Mapped[int] = mapped_column(ForeignKey('user_mail_accounts.user_mail_account_id'), nullable=False)
    access_token_txt: Mapped[str] = mapped_column(String(4096), nullable=False)
    refresh_token_txt: Mapped[str] = mapped_column(String(4096), nullable=True)
    expires_at_utc: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    created_at_utc: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    modified_at_utc: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    user_mail_account: Mapped["UserMailAccount"] = relationship(back_populates="oauth_token")
