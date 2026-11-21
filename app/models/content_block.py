from typing import TYPE_CHECKING
import uuid

from sqlalchemy import Enum as SAEnum, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.enums import BlockType
from base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from article_section import ArticleSection

class ContentBlock(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "content_block"
    __table_args__ = (
        UniqueConstraint("section_id", "position", name="uq_content_block_section_position")
    )
    
    section_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("article_section.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    block_type: Mapped[BlockType] = mapped_column(
        SAEnum(
            BlockType,
            name="block_type_enum",
            values_callable=lambda enum_cls: [item.value for item in enum_cls],
        ),
        nullable=False,
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False)

    context_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    code_lenguaje: Mapped[str | None] = mapped_column(String(60), nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    image_caption: Mapped[str | None] = mapped_column(String(300), nullable=True)

    section: Mapped["ArticleSection"] = relationship(back_populates="blocks")