import datetime
import uuid

from sqlalchemy import String, Boolean, DateTime, ForeignKey, func, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from api.models.base import Base


class UserMailAccount(Base):
    __tablename__ = "user_mail_accounts"

    user_mail_account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    email_address_txt: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    provider_cd: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    is_active_flg: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at_utc: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    modified_at_utc: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # one-to-one
    oauth_token: Mapped["OAuthToken"] = relationship(
        back_populates="user_mail_account",
        uselist=False,
        cascade="all, delete-orphan",
    )


class OAuthToken(Base):
    __tablename__ = "oauth_tokens"

    oauth_token_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_mail_account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user_mail_accounts.user_mail_account_id", ondelete="CASCADE"),
        nullable=False,
        unique=True,  # 🔑 enforces one-to-one at DB level
    )

    access_token_txt: Mapped[str] = mapped_column(
        String(4096),
        nullable=False,
    )

    refresh_token_txt: Mapped[str | None] = mapped_column(
        String(4096),
        nullable=True,
    )

    expires_at_utc: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    created_at_utc: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    modified_at_utc: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user_mail_account: Mapped["UserMailAccount"] = relationship(
        back_populates="oauth_token",
    )

