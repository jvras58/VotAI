"""Router for authentication endpoints."""

from fastapi import APIRouter, Request

from app.api.authentication.controller import AuthController
from app.api.authentication.schemas import AuthCallbackResponse

router = APIRouter()
controller = AuthController()


@router.get("/{provider}/login")
async def login(request: Request, provider: str):
    """Initiate OAuth login for the given provider."""
    return await controller.login(request, provider)


@router.get(
    "/{provider}/callback", response_model=AuthCallbackResponse, name="auth_callback"
)
async def auth_callback(request: Request, provider: str):
    """Handle OAuth callback for the given provider."""
    return await controller.callback(request, provider)
