"""Schemas for authentication."""

from pydantic import BaseModel


class AuthUserResponse(BaseModel):
    """Schema for authenticated user info response."""

    iss: str | None = None
    azp: str | None = None
    aud: str | None = None
    sub: str
    email: str
    email_verified: bool | None = None
    name: str | None = None
    picture: str | None = None
    given_name: str | None = None
    family_name: str | None = None
    locale: str | None = None


class AuthCallbackResponse(BaseModel):
    """Schema for auth callback response."""

    sub_hash: str
    email: str
    name: str | None = None
    picture: str | None = None
    access_token: str
    token_type: str = "bearer"
