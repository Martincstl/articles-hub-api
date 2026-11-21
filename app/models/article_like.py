from typing import TYPE_CHECKING
import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from base import Base, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from article import Article
    from user import User


class ArticleLike(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "article_like"
    __table_args__ = (
        UniqueConstraint("user_id", "article_id", name="uq_article_like_user_article"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    article_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("article.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    user: Mapped["User"] = relationship(back_populates="likes")
    article: Mapped["Article"] = relationship(back_populates="likes")