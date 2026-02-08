"""Controller for Poll-related operations."""

import hashlib

from fastapi import HTTPException

from app.utils.redis_client import redis_client


class PollController:
    """Controller for Poll-related operations."""

    VOTE_EXPIRATION_SECONDS: int = 86400 * 30  # 30 dias

    @staticmethod
    def vote(poll_id: str, user_sub: str, remote_ip: str) -> dict:
        """Register a vote, preventing duplicates via Redis."""
        sub_hash = hashlib.sha256(user_sub.encode()).hexdigest()
        key = f"voted:{poll_id}:{sub_hash}:{remote_ip}"

        if redis_client.exists(key):
            raise HTTPException(
                status_code=429,
                detail="Voto já feito",
            )

        redis_client.set(key, 1, ex=PollController.VOTE_EXPIRATION_SECONDS)
        # TODO: Salvar voto no banco de dados
        return {"sucesso": True}
