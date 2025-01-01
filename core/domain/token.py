from dataclasses import dataclass


@dataclass
class Token:
    token_type: str
    access_token: str
    expires_in: int
    refresh_token: str
    refresh_token_expires_in: int
