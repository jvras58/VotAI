"""Shared FastAPI dependencies for injection."""

from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app.utils.auth import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/google/login")


async def get_oauth_user(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    """
    Dependency that extracts and validates the current user from a Bearer token.

    Args:
        token: JWT Bearer token injected by FastAPI's OAuth2PasswordBearer.

    Returns:
        Dictionary with user's 'sub' claim.

    Raises:
        HTTPException 401: If the token is missing, invalid, or expired.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não autorizado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        sub: str | None = payload.get("sub")
        if sub is None:
            raise credentials_exception
        return {"sub": sub}
    except (JWTError, ValueError):
        raise credentials_exception


async def get_remote_address(request: Request) -> str:
    """
    Dependency that extracts the client's IP address from the request.

    Checks proxy headers first, then falls back to the direct client host.
    """
    ip = (
        request.headers.get("x-forwarded-for")
        or request.headers.get("x-real-ip")
        or request.headers.get("x-envoy-external-address")
        or (request.client.host if request.client else None)
    )
    return ip.split(",")[0].strip() if ip else "unknown"
