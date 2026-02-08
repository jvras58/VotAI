"""Controller for authentication operations."""

import hashlib

from fastapi import Request

from app.utils.auth import create_access_token
from app.utils.oauth_client import oauth


class AuthController:
    """Controller for Auth-related operations."""

    @staticmethod
    async def login(request: Request, provider: str):
        """Initiate OAuth login flow."""
        redirect_uri = request.url_for("auth_callback", provider=provider)
        client = getattr(oauth, provider)
        return await client.authorize_redirect(request, redirect_uri)

    @staticmethod
    async def callback(request: Request, provider: str) -> dict:
        """Handle OAuth callback, generate JWT, and return user info."""
        client = getattr(oauth, provider)
        token = await client.authorize_access_token(request)
        user = token.get("userinfo")

        sub_hash = hashlib.sha256(user["sub"].encode()).hexdigest()

        access_token = create_access_token(data={"sub": sub_hash})

        return {
            "sub_hash": sub_hash,
            "email": user.get("email"),
            "name": user.get("name"),
            "picture": user.get("picture"),
            "access_token": access_token,
            "token_type": "bearer",
        }
