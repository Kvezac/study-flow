from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt
from jwt.exceptions import InvalidTokenError as JwtInvalidTokenError

from app.application.interfaces.services.token_service import TokenService
from app.infrastructure.config import get_settings


class InvalidTokenError(Exception):
    pass


class JwtTokenService(TokenService):
    def __init__(self) -> None:
        settings = get_settings()
        self.secret_key = settings.jwt.secret_key
        self.algorithm = settings.jwt.algorithm
        self.access_token_expire_minutes = settings.jwt.access_token_expire_minutes

    def create_access_token(self, user_id: UUID, role: str) -> str:
        expires_at = datetime.now(UTC) + timedelta(
            minutes=self.access_token_expire_minutes,
        )
        payload = {
            "sub": str(user_id),
            "role": role,
            "exp": expires_at,
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def get_user_id(self, token: str) -> UUID:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except JwtInvalidTokenError as exc:
            raise InvalidTokenError("Token is invalid or expired.") from exc

        subject = payload.get("sub")
        if subject is None:
            raise InvalidTokenError("Token does not contain subject.")

        return UUID(subject)
