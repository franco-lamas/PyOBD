"""Custom exceptions for PyOBD."""


class BymaDataError(Exception):
    """Base exception for PyOBD."""

    pass


class APIError(BymaDataError):
    """API request failed."""

    pass


class ValidationError(BymaDataError):
    """Invalid parameters."""

    pass
