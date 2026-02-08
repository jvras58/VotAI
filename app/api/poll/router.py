"""Router for poll endpoints."""

from fastapi import APIRouter, Depends

from app.api.dependencies import get_oauth_user, get_remote_address
from app.api.poll.controller import PollController
from app.api.poll.schemas import VoteResponse

router = APIRouter()
controller = PollController()


@router.post("/{poll_id}/vote", response_model=VoteResponse)
async def vote(
    poll_id: str,
    user: dict = Depends(get_oauth_user),
    remote_ip: str = Depends(get_remote_address),
):
    """Register a vote for a poll."""
    return controller.vote(poll_id, user["sub"], remote_ip)
