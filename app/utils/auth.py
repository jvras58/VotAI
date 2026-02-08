"""JWT token creation and verification utilities."""

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt

from app.utils.settings import get_settings


def create_access_token(data: dict[str, Any], expires_delta: int | None = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: Payload data to encode in the token.
        expires_delta: Expiration time in seconds. Defaults to settings value.

    Returns:
        Encoded JWT string.
    """
    settings = get_settings()
    to_encode = data.copy()

    if expires_delta is not None:
        expire = datetime.now(timezone.utc) + timedelta(seconds=expires_delta)
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            seconds=settings.JWT_ACCESS_TOKEN_EXPIRE_SECONDS
        )

    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )


def decode_access_token(token: str) -> dict[str, Any]:
    """
    Decode and validate a JWT access token.

    Args:
        token: The JWT token string to decode.

    Returns:
        Decoded payload dictionary.

    Raises:
        JWTError: If the token is invalid or expired.
    """
    settings = get_settings()
    return jwt.decode(
        token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
    )
