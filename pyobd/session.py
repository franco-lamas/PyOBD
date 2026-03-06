"""Session management for BYMA Open Data API.

Based on Scrap_pyobd.ipynb session initialization pattern.
"""

import requests
import urllib3
import logging

urllib3.disable_warnings()
logger = logging.getLogger(__name__)


class BymaSession:
    """Manages HTTP session with BYMA API."""

    def __init__(self) -> None:
        self.session = requests.Session()
        self._initialize()

    def _initialize(self) -> None:
        """Initialize session with cookies and headers."""
        # Get initial cookies from dashboard
        self.session.get(
            "https://open.bymadata.com.ar/#/dashboard",
            verify=False,
        )

        # Set required headers (from notebook)
        self.session.headers.update({
            "Connection": "keep-alive",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="96"',
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/96.0.4664.110 Safari/537.36"
            ),
            "sec-ch-ua-platform": '"Windows"',
            "Origin": "https://open.bymadata.com.ar",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://open.bymadata.com.ar/",
            "Accept-Language": "es-US,es-419;q=0.9,es;q=0.8,en;q=0.7",
        })

        logger.debug("Session initialized with cookies and headers")

    def get(self, url: str, **kwargs) -> requests.Response:
        """GET request with SSL verification disabled."""
        kwargs.setdefault("verify", False)
        response = self.session.get(url, **kwargs)
        response.raise_for_status()
        return response

    def post(self, url: str, **kwargs) -> requests.Response:
        """POST request with SSL verification disabled."""
        kwargs.setdefault("verify", False)
        kwargs.setdefault("headers", self.session.headers)
        response = self.session.post(url, **kwargs)
        response.raise_for_status()
        return response

    def close(self) -> None:
        """Close the underlying session."""
        self.session.close()
