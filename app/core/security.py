from datetime import datetime, timedelta, timezone
import hashlib
import secrets
from typing import Any
from uuid import UUID

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from domain.enums import TokenType


def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
        subject: UUID  | str,
        expires_delta: timedelta | None = None,
        extra_claims: dict[str,Any] | None = None,
) -> str:

    now = datetime.now(timezone.utc)
    expire = now + (
        expires_delta
        if expires_delta is not None
        else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    playload: dict[str, Any] = {
        "sub": str(subject),
        "type": TokenType.ACCESS,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }
    if extra_claims:
        playload.update(extra_claims)

    return jwt.encode(playload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    

def decode_access_token(token: str) -> dict[str, Any]:
    try:
        playload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except JWTError as exc:
        raise ValueError("Invalid or expired access token") from exc

    if playload.get("type") != TokenType.ACCESS or not playload.get("sub"):
        raise ValueError("Malformed access token playload")
    return playload

def generate_refresh_token() -> str:
    return secrets.token_urlsafe(48)

def hash_refresh_token(raw_token: str) -> str:
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()

def get_refresh_token_expiration(days: int | None = None) -> datetime:
    total_days = days if days is not None else settings.REFRESH_TOKEN_EXPIRE_DAYS
    return datetime.now(timezone.utc) + timedelta(days=total_days)
    