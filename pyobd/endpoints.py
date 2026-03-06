"""BYMA Open Data API endpoints."""

BASE_URL = "https://open.bymadata.com.ar"

# General
MARKET_TIME = f"{BASE_URL}/vanoms-be-core/rest/api/bymadata/free/market-time"
INDEX_PRICE = f"{BASE_URL}/vanoms-be-core/rest/api/bymadata/free/index-price"
DICTIONARY = f"{BASE_URL}/assets/api/langs/es.json"

# Equity
LEADING_EQUITY = f"{BASE_URL}/vanoms-be-core/rest/api/bymadata/free/leading-equity"
GENERAL_EQUITY = f"{BASE_URL}/vanoms-be-core/rest/api/bymadata/free/general-equity"
CEDEARS = f"{BASE_URL}/vanoms-be-core/rest/api/bymadata/free/cedears"

# Current quote
CURRENT_QUOTE = (
    f"{BASE_URL}/vanoms-be-core/rest/api/bymadata/free"
    f"/bnown/fichatecnica/especies/cotizacion"
)

# Historical
HISTORICAL_SERIES = (
    f"{BASE_URL}/vanoms-be-core/rest/api/bymadata/free"
    f"/chart/historical-series/history"
)

# Fixed Income
PUBLIC_BONDS = f"{BASE_URL}/vanoms-be-core/rest/api/bymadata/free/public-bonds"
CORPORATE_BONDS = (
    f"{BASE_URL}/vanoms-be-core/rest/api/bymadata/free/negociable-obligations"
)
LETTERS = f"{BASE_URL}/vanoms-be-core/rest/api/bymadata/free/lebacs"

# Company data
COMPANY_GENERAL = (
    f"{BASE_URL}/vanoms-be-core/rest/api/bymadata/free"
    f"/bnown/fichatecnica/sociedades/general"
)
COMPANY_PROFILE = (
    f"{BASE_URL}/vanoms-be-core/rest/api/bymadata/free"
    f"/bnown/fichatecnica/especies/general"
)
COMPANY_MGMT = (
    f"{BASE_URL}/vanoms-be-core/rest/api/bymadata/free"
    f"/bnown/fichatecnica/sociedades/administracion"
)
COMPANY_BALANCE = (
    f"{BASE_URL}/vanoms-be-core/rest/api/bymadata/free/bolsar/balances"
)
