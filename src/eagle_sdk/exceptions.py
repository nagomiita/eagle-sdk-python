class EagleError(Exception):
    """Base exception for Eagle SDK."""


class EagleConnectionError(EagleError):
    """Raised when connection to Eagle API fails."""


class EagleApiError(EagleError):
    """Raised when Eagle API returns an error response."""

    def __init__(self, status: str, message: str = ""):
        self.status = status
        super().__init__(message or f"Eagle API error: {status}")
