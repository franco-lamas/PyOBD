"""Shared fixtures for PyOBD tests."""

import pytest

from pyobd import BymaData


@pytest.fixture(scope="session")
def client():
    """Shared BymaData client for the whole test session."""
    c = BymaData()
    yield c
    c.close()


@pytest.fixture
def sample_symbol():
    return "GGAL"
