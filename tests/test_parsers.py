"""Tests for exceptions module."""

from pyobd.exceptions import APIError, BymaDataError, ValidationError


def test_byma_data_error_is_exception():
    assert issubclass(BymaDataError, Exception)


def test_api_error_inherits():
    assert issubclass(APIError, BymaDataError)


def test_validation_error_inherits():
    assert issubclass(ValidationError, BymaDataError)


def test_api_error_message():
    err = APIError("request failed")
    assert str(err) == "request failed"
