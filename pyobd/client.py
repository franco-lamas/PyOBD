"""Main client class for BYMA Open Data.

Compatible with pyhomebroker API for drop-in replacement.
"""

import datetime
import json
import logging
from typing import Any, Dict, Optional

import pandas as pd
import pytz

from . import endpoints
from .exceptions import BymaDataError  # noqa: F401  (re-exported)
from .session import BymaSession

logger = logging.getLogger(__name__)


class BymaData:
    """
    BYMA Open Data client.

    Compatible with pyhomebroker API for drop-in replacement.

    Usage::

        >>> client = BymaData()
        >>> df = client.get_daily_history("GGAL", "2026-01-01", "2026-03-01")
    """

    def __init__(self) -> None:
        self.session = BymaSession()

    def __enter__(self) -> "BymaData":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def close(self) -> None:
        """Close session."""
        self.session.close()

    # ── General queries ────────────────────────────────────────────────

    def get_market_time(self) -> Dict[str, Any]:
        """Get market status and hours."""
        response = self.session.post(endpoints.MARKET_TIME, data="{}")
        return json.loads(response.text)

    def get_indices(self) -> pd.DataFrame:
        """Get equity indices (Merval, etc.)."""
        response = self.session.post(
            endpoints.INDEX_PRICE,
            data='{"Content-Type":"application/json"}',
        )
        data = json.loads(response.text)["data"]
        return pd.DataFrame(data)

    def get_dictionary(self) -> Dict[str, str]:
        """Get language dictionary (es.json)."""
        response = self.session.get(endpoints.DICTIONARY)
        return json.loads(response.text)

    # ── Equity data ────────────────────────────────────────────────────

    def get_bluechips(
        self,
        settlement_t2: bool = True,
        settlement_t1: bool = False,
        settlement_t0: bool = False,
        exclude_zero: bool = False,
    ) -> pd.DataFrame:
        """Get panel acciones líderes (blue chips)."""
        data = json.dumps(
            {
                "excludeZeroPxAndQty": exclude_zero,
                "T2": settlement_t2,
                "T1": settlement_t1,
                "T0": settlement_t0,
                "Content-Type": "application/json",
            }
        )
        response = self.session.post(endpoints.LEADING_EQUITY, data=data)
        return pd.DataFrame(json.loads(response.text)["data"])

    # backward compatibility
    def get_leading_equity(
        self,
        settlement_t2: bool = True,
        settlement_t1: bool = False,
        settlement_t0: bool = False,
        exclude_zero: bool = False,
    ) -> pd.DataFrame:
        """Deprecated alias for :meth:`get_bluechips`."""
        import warnings

        warnings.warn(
            "get_leading_equity() is deprecated, use get_bluechips()",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_bluechips(
            settlement_t2, settlement_t1, settlement_t0, exclude_zero
        )

    def get_general_board(self, settlement_t2: bool = True) -> pd.DataFrame:
        """Get panel acciones general (general board)."""
        data = json.dumps(
            {
                "excludeZeroPxAndQty": False,
                "T2": settlement_t2,
                "T1": False,
                "T0": False,
                "Content-Type": "application/json",
            }
        )
        response = self.session.post(endpoints.GENERAL_EQUITY, data=data)
        return pd.DataFrame(json.loads(response.text)["data"])

    # backward compatibility
    def get_general_equity(self, settlement_t2: bool = True) -> pd.DataFrame:
        """Deprecated alias for :meth:`get_general_board`."""
        import warnings

        warnings.warn(
            "get_general_equity() is deprecated, use get_general_board()",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_general_board(settlement_t2)

    def get_cedears(self, settlement_t2: bool = True) -> pd.DataFrame:
        """Get CEDEARs panel."""
        data = json.dumps(
            {
                "excludeZeroPxAndQty": False,
                "T2": settlement_t2,
                "T1": False,
                "T0": False,
                "Content-Type": "application/json",
            }
        )
        response = self.session.post(endpoints.CEDEARS, data=data)
        return pd.DataFrame(json.loads(response.text))

    def get_current_quote(
        self,
        symbol: str,
        settlement: str = "1",
    ) -> pd.DataFrame:
        """
        Get current quote for a symbol.

        Args:
            symbol: Ticker (e.g., "GGAL", "ALUA").
            settlement: "1" = CI, "2" = 24HS, "3" = 48HS
                        (also accepts "CI", "24HS", "48HS").

        Returns:
            DataFrame with current quote data.
        """
        settlement_map = {"CI": "1", "24HS": "2", "48HS": "3"}
        settlement_type = settlement_map.get(settlement.upper(), settlement)

        data = json.dumps(
            {
                "symbol": symbol,
                "settlementType": settlement_type,
                "Content-Type": "application/json",
            }
        )
        response = self.session.post(endpoints.CURRENT_QUOTE, data=data)
        return pd.DataFrame(json.loads(response.text)["data"])

    # ── Historical data (pyhomebroker compatible) ──────────────────────

    def get_daily_history(
        self,
        symbol: str,
        from_date: str,
        to_date: str,
        resolution: str = "D",
    ) -> pd.DataFrame:
        """
        Get historical OHLCV data.

        Compatible with pyhomebroker.history.get_daily_history().

        Args:
            symbol: Ticker with optional settlement (e.g., "AL30 48HS", "GGAL").
            from_date: Start date "YYYY-MM-DD".
            to_date: End date "YYYY-MM-DD".
            resolution: "D" (daily), "W" (weekly), "M" (monthly).

        Returns:
            DataFrame with: date, open, high, low, close, volume.
        """
        from_ts = self._date_to_timestamp(from_date)
        to_ts = self._date_to_timestamp(to_date)

        params = {
            "symbol": symbol,
            "resolution": resolution,
            "from": str(from_ts),
            "to": str(to_ts),
        }

        response = self.session.get(endpoints.HISTORICAL_SERIES, params=params)

        data = json.loads(response.text)

        # Handle "no_data" response from API
        if data.get("s") == "no_data" or not data.get("t"):
            logger.warning("No historical data for %s", symbol)
            return pd.DataFrame(
                columns=["date", "open", "high", "low", "close", "volume"]
            )

        df = pd.DataFrame(
            {
                "date": data["t"],
                "open": data["o"],
                "high": data["h"],
                "low": data["l"],
                "close": data["c"],
                "volume": data["v"],
            }
        )

        # Convert timestamp to date object (drop time)
        df["date"] = pd.to_datetime(df["date"], unit="s").dt.date
        df["volume"] = df["volume"].astype(int)

        return df

    def get_intraday_history(
        self,
        symbol: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        Get intraday (1-minute) historical OHLCV data.

        Compatible with pyhomebroker.history.get_intraday_history().

        Args:
            symbol: Ticker with optional settlement (e.g., "GGAL", "AL30 48HS").
            from_date: Start date "YYYY-MM-DD" (default: today).
            to_date: End date "YYYY-MM-DD" (default: from_date + 1 day).

        Returns:
            DataFrame with: date, open, high, low, close, volume.
            Date column includes time (datetime64[ns]).
        """
        # Default dates
        if from_date is None:
            from_date = datetime.datetime.now().strftime("%Y-%m-%d")
        if to_date is None:
            dt = datetime.datetime.strptime(from_date, "%Y-%m-%d")
            dt += datetime.timedelta(days=1)
            to_date = dt.strftime("%Y-%m-%d")

        from_ts = self._date_to_timestamp(from_date)
        to_ts = self._date_to_timestamp(to_date)

        params = {
            "symbol": symbol,
            "resolution": "1",  # 1-minute resolution
            "from": from_ts,
            "to": to_ts,
        }

        # reuse same endpoint as daily history; resolution=1 for 1-minute
        try:
            response = self.session.get(endpoints.HISTORICAL_SERIES, params=params)
            data = json.loads(response.text)
        except Exception as exc:
            logger.warning("intraday request failed for %s: %s", symbol, exc)
            return pd.DataFrame(
                columns=["date", "open", "high", "low", "close", "volume"]
            )

        if not data or data.get("s") != "ok":
            logger.warning("No intraday data for %s", symbol)
            return pd.DataFrame(
                columns=["date", "open", "high", "low", "close", "volume"]
            )

        df = pd.DataFrame(
            {
                "date": data["t"],
                "open": data["o"],
                "high": data["h"],
                "low": data["l"],
                "close": data["c"],
                "volume": data["v"],
            }
        )

        df["date"] = pd.to_datetime(df["date"], unit="s")
        df["volume"] = df["volume"].astype(int)

        return df

    # ── Fixed Income ───────────────────────────────────────────────────

    def get_government_bonds(self, settlement_t2: bool = True) -> pd.DataFrame:
        """Get títulos públicos (renamed from get_public_bonds)."""
        data = json.dumps(
            {
                "T2": settlement_t2,
                "T1": False,
                "T0": False,
                "Content-Type": "application/json",
            }
        )
        response = self.session.post(endpoints.PUBLIC_BONDS, data=data)
        return pd.DataFrame(json.loads(response.text)["data"])

    # backward compatibility
    def get_public_bonds(self, settlement_t2: bool = True) -> pd.DataFrame:
        """Deprecated alias for :meth:`get_government_bonds`."""
        import warnings

        warnings.warn(
            "get_public_bonds() is deprecated, use get_government_bonds()",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_government_bonds(settlement_t2)

    def get_corporate_bonds(self, settlement_t2: bool = True) -> pd.DataFrame:
        """Get obligaciones negociables."""
        data = json.dumps(
            {
                "excludeZeroPxAndQty": False,
                "T2": settlement_t2,
                "T1": False,
                "T0": False,
                "Content-Type": "application/json",
            }
        )
        response = self.session.post(endpoints.CORPORATE_BONDS, data=data)
        return pd.DataFrame(json.loads(response.text))

    def get_short_term_government_bonds(
        self, settlement_t2: bool = True
    ) -> pd.DataFrame:
        """Get letras (short-term government bonds)."""
        data = json.dumps(
            {
                "excludeZeroPxAndQty": False,
                "T2": settlement_t2,
                "T1": False,
                "T0": False,
                "Content-Type": "application/json",
            }
        )
        response = self.session.post(endpoints.LETTERS, data=data)
        return pd.DataFrame(json.loads(response.text)["data"])

    # backward compatibility
    def get_letters(self, settlement_t2: bool = True) -> pd.DataFrame:
        """Deprecated alias for :meth:`get_short_term_government_bonds`."""
        import warnings

        warnings.warn(
            "get_letters() is deprecated, use get_short_term_government_bonds()",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_short_term_government_bonds(settlement_t2)

    # ── Company information ────────────────────────────────────────────

    def get_company_info(self, symbol: str) -> pd.DataFrame:
        """Get company/society general information.

        Data includes: address, website, phone, establishment date, etc.

        Args:
            symbol: Ticker or company symbol.

        Returns:
            DataFrame with two columns: 'campo' (field name) and 'valor' (value).
            One row per field.
        """
        data = json.dumps(
            {
                "symbol": symbol,
                "Content-Type": "application/json",
            }
        )
        response = self.session.post(endpoints.COMPANY_GENERAL, data=data)
        result = json.loads(response.text)
        if result.get("data"):
            # Extract the first record and convert to campo/valor format
            record = result["data"][0]
            df_data = [{"campo": k, "valor": v} for k, v in record.items()]
            return pd.DataFrame(df_data)
        return pd.DataFrame(columns=["campo", "valor"])

    def get_equity_profile(self, symbol: str) -> pd.DataFrame:
        """Get equity/species technical data.

        Data includes: ISIN code, species type, denomination, market cap, etc.

        Args:
            symbol: Ticker.

        Returns:
            DataFrame with two columns: 'campo' (field name) and 'valor' (value).
            One row per field.
        """
        data = json.dumps(
            {
                "symbol": symbol,
                "Content-Type": "application/json",
            }
        )
        response = self.session.post(endpoints.COMPANY_PROFILE, data=data)
        result = json.loads(response.text)
        if result.get("data"):
            # Extract the first record and convert to campo/valor format
            record = result["data"][0]
            df_data = [{"campo": k, "valor": v} for k, v in record.items()]
            return pd.DataFrame(df_data)
        return pd.DataFrame(columns=["campo", "valor"])

    def get_company_management(self, symbol: str) -> pd.DataFrame:
        """Get company management/directors."""
        data = json.dumps(
            {
                "symbol": symbol,
                "Content-Type": "application/json",
            }
        )
        response = self.session.post(endpoints.COMPANY_MGMT, data=data)
        result = json.loads(response.text)
        return pd.DataFrame(result.get("data", []))

    def get_company_balance(self, symbol: str) -> pd.DataFrame:
        """Get latest company balance sheet.

        Note:
            This endpoint may redirect to an internal BYMA host that is
            not reachable from all networks.  Returns an empty DataFrame
            on connection errors.
        """
        params = {"symbol": symbol}
        try:
            response = self.session.get(endpoints.COMPANY_BALANCE, params=params)
        except Exception as exc:
            logger.warning("company_balance unreachable: %s", exc)
            return pd.DataFrame()

        result = json.loads(response.text)
        if result.get("data"):
            return pd.DataFrame(result["data"][0]["Cuentas"])
        return pd.DataFrame()

    # ── Helpers ────────────────────────────────────────────────────────

    @staticmethod
    def _date_to_timestamp(date_str: str) -> int:
        """Convert 'YYYY-MM-DD' to Unix timestamp (Buenos Aires TZ)."""
        dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        tz = pytz.timezone("America/Argentina/Buenos_Aires")
        dt = tz.localize(dt)
        return int(dt.timestamp())
