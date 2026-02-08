"""Router for poll endpoints."""

from fastapi import APIRouter, Depends, Request

from app.api.poll.controller import PollController
from app.api.poll.schemas import VoteResponse

router = APIRouter()
controller = PollController()


# TODO: Implementar get_oauth_user e get_remote_address como dependências
async def get_oauth_user():
    """Placeholder: será implementado posteriormente."""
    raise NotImplementedError


async def get_remote_address(request: Request) -> str:
    """Extract the client's IP address from the request."""
    ip = (
        request.headers.get("x-forwarded-for")
        or request.headers.get("x-real-ip")
        or request.headers.get("x-envoy-external-address")
        or request.client.host
    )
    return ip.split(",")[0].strip() if ip else "unknown"


@router.post("/{poll_id}/vote", response_model=VoteResponse)
async def vote(
    poll_id: str,
    user_sub: str = Depends(get_oauth_user),
    remote_ip: str = Depends(get_remote_address),
):
    """Register a vote for a poll."""
    return controller.vote(poll_id, user_sub, remote_ip)
