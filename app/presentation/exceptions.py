class PresentationError(Exception):
    """Base exception for presentation-layer errors."""


class AuthenticationError(PresentationError):
    pass


class PermissionDeniedError(PresentationError):
    pass
