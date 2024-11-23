from typing import Annotated
from fastapi import HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer

from common.constants import Role
from common.models import CurrentUser
from utils.jwt_utils import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = decode_access_token(token)

    user_id = payload.get("user_id")
    role = payload.get("role")
    if not user_id or not role or role != Role.USER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return CurrentUser(user_id, Role(role))
