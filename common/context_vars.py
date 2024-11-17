from contextvars import ContextVar
from typing import Optional

from common.models import CurrentUser

user_context: ContextVar[Optional[CurrentUser]] = ContextVar("current_user", default=None)
