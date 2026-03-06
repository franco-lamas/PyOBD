"""Tests for BymaSession."""

from pyobd.session import BymaSession


class TestBymaSession:
    def test_session_creates(self):
        s = BymaSession()
        assert s.session is not None
        s.close()

    def test_session_has_headers(self):
        s = BymaSession()
        headers = s.session.headers
        assert "User-Agent" in headers
        assert "Content-Type" in headers
        assert headers["Content-Type"] == "application/json"
        s.close()

    def test_session_has_cookies(self):
        s = BymaSession()
        # Should have obtained cookies from initial GET
        assert s.session.cookies is not None
        s.close()
