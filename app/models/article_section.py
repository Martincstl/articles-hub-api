from typing import TYPE_CHECKING
import uuid

from sqlalchemy import ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.article import Article
    from app.models.content_block import ContentBlock


class ArticleSection(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "article_section"
    __table_args__ = (
        UniqueConstraint("article_id", "position", name="uq_article_section_article_position"),
    )

    article_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("article.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    heading: Mapped[str] = mapped_column(String(200), nullable=False)
    body: Mapped[str | None] = mapped_column(Text, nullable=True)
    position: Mapped[int] = mapped_column(Integer, nullable=False)

    article: Mapped["Article"] = relationship(back_populates="sections")
    blocks: Mapped[list["ContentBlock"]] = relationship(
        back_populates="section",
        cascade="all, delete-orphan",
        order_by="ContentBlock.position",
    )