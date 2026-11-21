from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.article import Article
    from app.models.article_like import ArticleLike
    from app.models.follow import Follow
    from app.models.refresh_token import RefreshToken

class User (UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    display_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True) 
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true",nullable=False)

    refreshtokens: Mapped[list["RefreshToken"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    articles: Mapped[list["Article"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",
    )
    following_links: Mapped[list["Follow"]] = relationship(
        foreign_keys="Follow.follower_id",
        back_populates="follower",
        cascade="all, delete-orphan",
    )
    follower_links: Mapped[list["Follow"]] = relationship(
        foreign_keys="Follow.following_id",
        back_populates="following",
        cascade="all, delete-orphan",
    )
    likes: Mapped[list["ArticleLike"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )