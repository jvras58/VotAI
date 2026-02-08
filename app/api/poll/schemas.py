"""Schemas for poll operations."""

from pydantic import BaseModel


class VoteRequest(BaseModel):
    """Schema for a vote request."""

    option_id: str | None = None


class VoteResponse(BaseModel):
    """Schema for a vote response."""

    sucesso: bool
