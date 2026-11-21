import uuid

from sqlalchemy import exists, func, select
from sqlalchemy.orm import Session

from app.models.follow import Follow
from app.repositories.base import BaseRepository

class FollowRepository(BaseRepository[Follow]):
    def __init__(self, db: Session) -> None:
        super().__init__(db,Follow)

    def get_by_pair(
            self,
            follower_id: uuid.UUID,
            following_id: uuid.UUID,
    ) -> Follow | None:
        stmt = select(Follow).where(
            Follow.follower_id == follower_id,
            Follow.following_id == following_id,
        )
        return self.db.scalar(stmt)

    def exists_follow(
            self,
            follower_id: uuid.UUID,
            following_id: uuid.UUID,
    ) -> bool:
        stmt = select(
            exists().where(
                Follow.follower_id == following_id,
                Follow.following_id == following_id,
            )
        )
        return bool(self.db.scalar(stmt))

    def count_followers(self, user_id: uuid.UUID) -> int:
        stmt = select(func.count()).select_from(Follow).where(Follow.following_id == user_id)
        return int(self.db.scalar(stmt) or 0)

    def count_following(self, user_id: uuid.UUID) -> int:
        stmt = select(func.count()).select_from(Follow).where(Follow.follower_id == user_id)
        return int(self.db.scalar(stmt) or 0)
    
    def list_follower_ids(
            self,
            user_id: uuid.UUID,
            limit: int = 50,
            offset: int = 0,
    ) -> list[uuid.UUID]:
        stmt = (
            select(Follow.follower_id)
            .where(Follow.following_id == user_id)
            .order_by(Follow.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(self.db.scalars(stmt).all())

    def list_following_ids(
            self,
            user_id: uuid.UUID,
            limit: int = 50,
            offset: int = 0,
    ) -> list[uuid.UUID]:
        stmt = (
            select(Follow.following_id)
            .where(Follow.follower_id == user_id)
            .order_by(Follow.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(self.db.scalars(stmt).all())

    