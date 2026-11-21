import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.domain.enums import ArticleStatus
from app.models.article import Article
from app.models.article_section import ArticleSection
from app.repositories.base import BaseRepository

class ArticleRepository(BaseRepository[Article]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Article)

    def get_by_slug(self, slug: str) -> Article | None:
        stmt = (
            select(Article)
            .where(Article.slug == slug)
            .options(
                selectinload(Article.sections).selectinload(ArticleSection.blocks)
            )
        )
        return self.db.scalar(stmt)

    def get_with_tree(self, article_id: uuid.UUID) -> Article | None:
        stmt = (
            select(Article)
            .where(Article.id == article_id)
            .options(
                selectinload(Article.sections).selectinload(ArticleSection.blocks)
            )
        )
        return self.db.scalar(stmt)

    def list_published(self, limit: int = 20, offset: int = 0) -> list[Article]:
        stmt = (
            select(Article)
            .where(Article.status == ArticleStatus.PUBLISHED)
            .order_by(Article.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(self.db.scalars(stmt).all())