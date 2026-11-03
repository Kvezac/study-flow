class ApplicationError(Exception):
    """Base exception for application-layer errors."""


class CourseNotFoundError(ApplicationError):
    pass


class LectureNotFoundError(ApplicationError):
    pass
