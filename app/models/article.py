from datetime import datetime
from typing import TYPE_CHECKING
import uuid

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.enums import ArticleStatus
from base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from article_like import ArticleLike
    from article_section import ArticleSection
    from user import User

class Article(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "article"

    author_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(220), unique=True, index=True, nullable=False)
    summary: Mapped[str | None] = mapped_column(String(500), nullable=True)
    cover_image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    status: Mapped[ArticleStatus] = mapped_column(
        SAEnum(
            ArticleStatus,
            name="article_status_enum",
            values_callable=lambda enum_cls: [item.value for item in enum_cls],
        ),
        default=ArticleStatus.DRAFT,
        server_default=ArticleStatus.DRAFT.value,
        index=True,
        nullable=False,
    ) 
    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    author: Mapped["User"] = relationship(back_populates="articles")
    sections: Mapped[list["ArticleSection"]] = relationship(
        back_populates="article",
        cascade="all, delete-orphan",
        order_by="ArticleSection.position",
    )
    likes: Mapped[list["ArticleLike"]] = relationship(
        back_populates="article",
        cascade="all, delete-orphan",
    )