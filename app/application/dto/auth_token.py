from dataclasses import dataclass


@dataclass(slots=True)
class AuthToken:
    access_token: str
    token_type: str = "bearer"
