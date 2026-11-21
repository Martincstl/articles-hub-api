from datetime import datetime, timezone
import uuid

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.models.refresh_token import RefreshToken
from app.repositories.base import BaseRepository

class RefreshTokenRepository(BaseRepository[RefreshToken]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, RefreshToken)

    def get_by_jti(self, jti: str) -> RefreshToken | None:
        stmt = select(RefreshToken).where(RefreshToken.jti == jti)
        return self.db.scalar(stmt)

    def get_by_token_hash(self, token_hash: str) -> RefreshToken | None:
        stmt = select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        return self.db.scalar(stmt)

    def get_active_by_token_hash(
            self,
            token_hash: str,
            now: datetime | None = None,
    ) -> RefreshToken | None:
        current_time = now or datetime.now(timezone.utc)
        stmt = select(RefreshToken).where(
            RefreshToken.token_hash == token_hash,
            RefreshToken.revoked_at.is_(None),
            RefreshToken.expires_at > current_time,
        )
        return self.db.scalar(stmt)

    def revoke_token(
            self,
            token: RefreshToken,
            revoked_at: datetime | None = None,
            replaced_by_id: uuid.UUID | None = None,
    ) -> RefreshToken:
        token.revoked_at = revoked_at or datetime.now(timezone.utc)
        if replaced_by_id is not None:
            token.replaced_by_id = replaced_by_id
        return token

    def revoke_all_for_user(
        self,
        user_id: uuid.UUID,
        revoked_at: datetime | None = None,
    ) -> int:
        current_time = revoked_at or datetime.now(timezone.utc)
        stmt = (
            update(RefreshToken)
            .where(
                RefreshToken.user_id == user_id,
                RefreshToken.revoked_at.is_(None),
            )
            .values(revoked_at=current_time)
        )
        result = self.db.execute(stmt)
        return int(result.rowcount or 0)