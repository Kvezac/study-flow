from uuid import uuid4

import pytest

from app.domain.entities.user import User, UserRole
from app.domain.exceptions import InvalidUserError


def test_user_is_created_with_valid_data() -> None:
    user = User(
        id=uuid4(),
        email="user@example.com",
        hashed_password="hashed-password",
        role=UserRole.STUDENT,
    )

    assert user.email == "user@example.com"
    assert user.role is UserRole.STUDENT


def test_user_raises_error_when_email_is_invalid() -> None:
    with pytest.raises(InvalidUserError):
        User(
            id=uuid4(),
            email="invalid-email",
            hashed_password="hashed-password",
            role=UserRole.STUDENT,
        )


def test_user_raises_error_when_hashed_password_is_blank() -> None:
    with pytest.raises(InvalidUserError):
        User(
            id=uuid4(),
            email="user@example.com",
            hashed_password="   ",
            role=UserRole.STUDENT,
        )


def test_admin_user_can_manage_platform() -> None:
    user = User(
        id=uuid4(),
        email="admin@example.com",
        hashed_password="hashed-password",
        role=UserRole.ADMIN,
    )

    assert user.is_admin() is True
    assert user.can_manage_platform() is True
    assert user.can_manage_content() is True


def test_student_can_take_learning_activities_but_cannot_manage_platform() -> None:
    user = User(
        id=uuid4(),
        email="student@example.com",
        hashed_password="hashed-password",
        role=UserRole.STUDENT,
    )

    assert user.can_take_learning_activities() is True
    assert user.can_manage_platform() is False
