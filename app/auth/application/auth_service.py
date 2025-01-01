from fastapi import HTTPException
from starlette import status

from app.auth.domain.token import Token
from common.constants import Role
from utils.jwt_utils import create_access_token, decode_access_token
from common.config import get_settings


config = get_settings()


class AuthService:
    @staticmethod
    async def generate_tokens(user_id: str) -> Token:
        access_token = create_access_token(
            payload={"user_id": user_id}, role=Role.USER, expires_delta=config.access_token_expires_days
        )
        refresh_token = create_access_token(
            payload={"user_id": user_id}, role=Role.USER, expires_delta=config.refresh_token_expires_days
        )
        expires_in = config.access_token_expires_days.total_seconds()
        refresh_token_expires_in = config.refresh_token_expires_days.total_seconds()
        return Token(
            token_type="bearer",
            access_token=access_token,
            expires_in=expires_in,
            refresh_token=refresh_token,
            refresh_token_expires_in=refresh_token_expires_in,
        )

    async def refresh_access_token(self, user_id: str, refresh_token: str) -> Token:
        payload = decode_access_token(refresh_token)
        if payload["user_id"] != user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return await self.generate_tokens(user_id=user_id)
