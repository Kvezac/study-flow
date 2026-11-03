from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID

from app.domain.exceptions import InvalidUserError


class UserRole(StrEnum):
    STUDENT = "student"
    AUTHOR = "author"
    ADMIN = "admin"


@dataclass(slots=True)
class User:
    id: UUID
    email: str
    hashed_password: str
    role: UserRole

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if not self.email or "@" not in self.email:
            raise InvalidUserError("User email is invalid.")
        if not self.hashed_password or not self.hashed_password.strip():
            raise InvalidUserError("User hashed password cannot be empty.")

    def is_admin(self) -> bool:
        return self.role is UserRole.ADMIN

    def is_author(self) -> bool:
        return self.role is UserRole.AUTHOR

    def is_student(self) -> bool:
        return self.role is UserRole.STUDENT

    def can_manage_platform(self) -> bool:
        return self.is_admin()

    def can_manage_learning_content(self) -> bool:
        return self.role in {UserRole.ADMIN, UserRole.AUTHOR}

    def can_take_learning_activities(self) -> bool:
        return self.is_student()

    def can_manage_content(self) -> bool:
        return self.can_manage_platform()
