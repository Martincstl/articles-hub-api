from typing import TYPE_CHECKING
import uuid

from sqlalchemy import ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from article import Article
    from content_block import ContentBlock


class ArticleSection(TimestampMixin, Base):
    __tablename__ = "article_section"
    __table_args__ = (
        UniqueConstraint("article_id", "sort_order", name="uq_article_section_article_sort_order"),
    )

    section_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    article_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("article.article_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    heading: Mapped[str] = mapped_column(String(200), nullable=False)
    body: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False)

    article: Mapped["Article"] = relationship(back_populates="sections")
    blocks: Mapped[list["ContentBlock"]] = relationship(
        back_populates="section",
        cascade="all, delete-orphan",
        order_by="ContentBlock.sort_order",
    )