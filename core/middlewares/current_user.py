from fastapi import Request
from core.logger import logger

from common.context_vars import user_context
from common.models import CurrentUser
from utils.jwt_utils import decode_access_token


def get_current_user_middleware(request: Request, call_next):
    authorization = request.headers.get("Authorization")
    if authorization:
        splits = authorization.split(" ")
        if splits[0] == "Bearer":
            token = splits[1]
            payload = decode_access_token(token)
            user_id = payload.get("user_id")
            user_role = payload.get("role")
            user_context.set(CurrentUser(id=user_id, role=user_role))
    logger.info(request.url)
    response = call_next(request)
    return response
