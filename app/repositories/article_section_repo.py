import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.article_section import ArticleSection
from app.repositories.base import BaseRepository


class ArticleSectionRepository(BaseRepository[ArticleSection]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, ArticleSection)

    def list_by_article(
        self,
        article_id: uuid.UUID,
        include_blocks: bool = False,
    ) -> list[ArticleSection]:
        stmt = (
            select(ArticleSection)
            .where(ArticleSection.article_id == article_id)
            .order_by(ArticleSection.position.asc())
        )
        if include_blocks:
            stmt = stmt.options(selectinload(ArticleSection.blocks))
        return list(self.db.scalars(stmt).all())

    def get_by_article_and_position(
        self,
        article_id: uuid.UUID,
        position: int,
    ) -> ArticleSection | None:
        stmt = select(ArticleSection).where(
            ArticleSection.article_id == article_id,
            ArticleSection.position == position,
        )
        return self.db.scalar(stmt)

    def get_next_position(self, article_id: uuid.UUID) -> int:
        stmt = (
            select(func.max(ArticleSection.position))
            .where(ArticleSection.article_id == article_id)
        )
        max_position = self.db.scalar(stmt)
        return (max_position + 1) if max_position is not None else 0