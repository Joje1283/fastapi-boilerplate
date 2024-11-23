from fastapi import HTTPException
from starlette import status

from app.auth.domain.token import Token
from common.constants import Role
from utils.jwt_utils import create_access_token, decode_access_token
from core.config import get_settings


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
        return Token(access_token=access_token, refresh_token=refresh_token)

    async def refresh_access_token(self, user_id: str, token: Token) -> Token:
        payload = decode_access_token(token.refresh_token)
        if payload["user_id"] != user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return await self.generate_tokens(user_id=user_id)
