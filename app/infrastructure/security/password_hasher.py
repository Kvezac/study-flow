from pwdlib import PasswordHash

from app.application.interfaces.services.password_hasher import PasswordHasher


class PwdlibPasswordHasher(PasswordHasher):
    def __init__(self) -> None:
        self.password_hash = PasswordHash.recommended()

    def hash(self, raw_password: str) -> str:
        return self.password_hash.hash(raw_password)

    def verify(self, raw_password: str, hashed_password: str) -> bool:
        return self.password_hash.verify(raw_password, hashed_password)
