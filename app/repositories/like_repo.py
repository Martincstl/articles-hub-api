import uuid

from sqlalchemy import exists, func, select
from sqlalchemy.orm import Session

from app.models.article_like import ArticleLike
from app.repositories.base import BaseRepository


class ArticleLikeRepository(BaseRepository[ArticleLike]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, ArticleLike)

    def get_by_user_and_article(
        self,
        user_id: uuid.UUID,
        article_id: uuid.UUID,
    ) -> ArticleLike | None:
        stmt = select(ArticleLike).where(
            ArticleLike.user_id == user_id,
            ArticleLike.article_id == article_id,
        )
        return self.db.scalar(stmt)

    def exists_like(
        self,
        user_id: uuid.UUID,
        article_id: uuid.UUID,
    ) -> bool:
        stmt = select(
            exists().where(
                ArticleLike.user_id == user_id,
                ArticleLike.article_id == article_id,
            )
        )
        return bool(self.db.scalar(stmt))

    def count_by_article(self, article_id: uuid.UUID) -> int:
        stmt = (
            select(func.count())
            .select_from(ArticleLike)
            .where(ArticleLike.article_id == article_id)
        )
        return int(self.db.scalar(stmt) or 0)

    def count_by_user(self, user_id: uuid.UUID) -> int:
        stmt = (
            select(func.count())
            .select_from(ArticleLike)
            .where(ArticleLike.user_id == user_id)
        )
        return int(self.db.scalar(stmt) or 0)