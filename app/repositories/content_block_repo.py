import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.content_block import ContentBlock
from app.repositories.base import BaseRepository


class ContentBlockRepository(BaseRepository[ContentBlock]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, ContentBlock)

    def list_by_section(self, section_id: uuid.UUID) -> list[ContentBlock]:
        stmt = (
            select(ContentBlock)
            .where(ContentBlock.section_id == section_id)
            .order_by(ContentBlock.position.asc())
        )
        return list(self.db.scalars(stmt).all())

    def get_by_section_and_position(
        self,
        section_id: uuid.UUID,
        position: int,
    ) -> ContentBlock | None:
        stmt = select(ContentBlock).where(
            ContentBlock.section_id == section_id,
            ContentBlock.position == position,
        )
        return self.db.scalar(stmt)

    def get_next_position(self, section_id: uuid.UUID) -> int:
        stmt = (
            select(func.max(ContentBlock.position))
            .where(ContentBlock.section_id == section_id)
        )
        max_pos = self.db.scalar(stmt)
        return (max_pos + 1) if max_pos is not None else 0