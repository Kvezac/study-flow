from uuid import uuid4

import pytest

from app.domain.entities.section import Section
from app.domain.exceptions import InvalidSectionError


def test_section_is_created_with_valid_data() -> None:
    section = Section(
        id=uuid4(),
        module_id=uuid4(),
        title="Section 1",
        description="",
        position=1,
    )

    assert section.title == "Section 1"
    assert section.description == ""
    assert section.lecture_ids == []


def test_section_raises_error_when_title_is_blank() -> None:
    with pytest.raises(InvalidSectionError):
        Section(
            id=uuid4(),
            module_id=uuid4(),
            title="   ",
            description="Anything",
            position=1,
        )


def test_section_raises_error_when_position_is_not_positive() -> None:
    with pytest.raises(InvalidSectionError):
        Section(
            id=uuid4(),
            module_id=uuid4(),
            title="Section 1",
            description="Anything",
            position=0,
        )
