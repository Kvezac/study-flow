class DomainError(Exception):
    """Base exception for domain-layer violations."""


class InvalidCourseError(DomainError):
    pass


class InvalidModuleError(DomainError):
    pass


class InvalidSectionError(DomainError):
    pass


class InvalidLectureError(DomainError):
    pass


class InvalidUserError(DomainError):
    pass
