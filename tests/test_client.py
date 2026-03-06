"""Tests for BymaData client — integration tests against the live API."""

import pandas as pd
import pytest

from pyobd import BymaData


# ── Initialization ─────────────────────────────────────────────────────


class TestClientInit:
    def test_client_creates_session(self, client):
        assert client is not None
        assert client.session is not None

    def test_context_manager(self):
        with BymaData() as c:
            assert c.session is not None


# ── General queries ────────────────────────────────────────────────────


class TestGeneralQueries:
    def test_market_time(self, client):
        result = client.get_market_time()
        assert "marketOpeningTime" in result
        assert "marketClosingTime" in result

    def test_get_indices(self, client):
        df = client.get_indices()
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert "symbol" in df.columns

    def test_get_dictionary(self, client):
        d = client.get_dictionary()
        assert isinstance(d, dict)
        assert len(d) > 0


# ── Equity data ────────────────────────────────────────────────────────


class TestEquityData:
    def test_bluechips_returns_dataframe(self, client):
        df = client.get_bluechips()
        assert isinstance(df, pd.DataFrame)
        # alias should still work
        df2 = client.get_leading_equity()
        assert isinstance(df2, pd.DataFrame)

    def test_general_board_returns_dataframe(self, client):
        df = client.get_general_board()
        assert isinstance(df, pd.DataFrame)
        df2 = client.get_general_equity()
        assert isinstance(df2, pd.DataFrame)

    def test_cedears_returns_dataframe(self, client):
        df = client.get_cedears()
        assert isinstance(df, pd.DataFrame)

    def test_current_quote_settlement_mapping(self, client):
        # Just verify it doesn't crash — data may be empty outside market hours
        df = client.get_current_quote("GGAL", settlement="48HS")
        assert isinstance(df, pd.DataFrame)


# ── Historical data ───────────────────────────────────────────────────


class TestHistoricalData:
    def test_daily_history_with_data(self, client):
        df = client.get_daily_history("GGAL 24HS", "2025-06-01", "2025-12-31")
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        expected_cols = ["date", "open", "high", "low", "close", "volume"]
        assert list(df.columns) == expected_cols
        assert df["date"].dtype == object

    def test_daily_history_no_data(self, client):
        df = client.get_daily_history("GGAL 48HS", "2020-01-01", "2020-01-02")
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0
        assert "date" in df.columns

    def test_date_to_timestamp(self):
        ts = BymaData._date_to_timestamp("2025-01-01")
        assert isinstance(ts, int)
        assert ts > 0

    def test_intraday_history(self, client):
        # this is a live query and may return 0 rows outside market hours
        df = client.get_intraday_history("GGAL")
        assert isinstance(df, pd.DataFrame)
        assert "date" in df.columns
        # dtype should include time if not empty
        if len(df) > 0:
            assert df["date"].dtype == "datetime64[ns]"


# ── Fixed Income ───────────────────────────────────────────────────────


class TestFixedIncome:
    def test_government_bonds_returns_dataframe(self, client):
        df = client.get_government_bonds()
        assert isinstance(df, pd.DataFrame)
        df2 = client.get_public_bonds()
        assert isinstance(df2, pd.DataFrame)

    def test_corporate_bonds_returns_dataframe(self, client):
        df = client.get_corporate_bonds()
        assert isinstance(df, pd.DataFrame)

    def test_short_term_government_bonds_returns_dataframe(self, client):
        df = client.get_short_term_government_bonds()
        assert isinstance(df, pd.DataFrame)
        df2 = client.get_letters()
        assert isinstance(df2, pd.DataFrame)


# ── Company information ───────────────────────────────────────────────


class TestCompanyInfo:
    def test_company_info(self, client):
        df = client.get_company_info("ALUA")
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == ["campo", "valor"]

    def test_equity_profile(self, client):
        df = client.get_equity_profile("ALUA")
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == ["campo", "valor"]

    def test_company_management(self, client):
        df = client.get_company_management("ALUA")
        assert isinstance(df, pd.DataFrame)

    def test_company_balance(self, client):
        try:
            df = client.get_company_balance("ALUA")
            assert isinstance(df, pd.DataFrame)
        except Exception:
            # The balance endpoint may redirect to an internal host
            # not reachable from all environments
            pytest.skip("company_balance endpoint not reachable")
