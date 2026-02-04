import datetime
import uuid
from sqlalchemy import String, Boolean, DateTime, ForeignKey, func, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


# SQLAlchemy model for storing user mail account information.
# This table (`user_mail_accounts`) holds details about each email account
# linked through OAuth, such as the email address, provider, and active status.
class UserMailAccount(Base):
    __tablename__ = "user_mail_accounts"

    # Primary key for the user mail account.
    user_mail_account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    # The email address associated with the account, must be unique.
    email_address_txt: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False
    )
    # The provider code (e.g., Google, Microsoft) for this mail account, referenced from an enum.
    provider_cd: Mapped[int] = mapped_column(Integer, nullable=False)
    # Flag indicating if the mail account is active. Defaults to True.
    is_active_flg: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    # Timestamp for when the record was created, set to UTC now by default.
    created_at_utc: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    # Timestamp for when the record was last modified, updated on each change.
    modified_at_utc: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Defines a one-to-one relationship with the OAuthToken model.
    # `back_populates` ensures two-way linking between UserMailAccount and OAuthToken.
    oauth_token: Mapped["OAuthToken"] = relationship(back_populates="user_mail_account")


# SQLAlchemy model for storing OAuth tokens associated with user mail accounts.
# This table (`oauth_tokens`) stores sensitive access and refresh tokens, linked
# to a specific `UserMailAccount`.
class OAuthToken(Base):
    __tablename__ = "oauth_tokens"

    # Primary key for the OAuth token record.
    oauth_token_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    # Foreign key linking this token to a `UserMailAccount`.
    user_mail_account_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_mail_accounts.user_mail_account_id"), nullable=False
    )
    # The access token obtained from the OAuth provider.
    access_token_txt: Mapped[str] = mapped_column(String(4096), nullable=False)
    # The refresh token obtained from the OAuth provider, which can be null if not provided.
    refresh_token_txt: Mapped[str] = mapped_column(String(4096), nullable=True)
    # Timestamp indicating when the access token expires.
    expires_at_utc: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    # Timestamp for when the record was created, set to UTC now by default.
    created_at_utc: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    # Timestamp for when the record was last modified, updated on each change.
    modified_at_utc: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Defines a one-to-one relationship with the UserMailAccount model.
    # `back_populates` ensures two-way linking between OAuthToken and UserMailAccount.
    user_mail_account: Mapped["UserMailAccount"] = relationship(
        back_populates="oauth_token"
    )