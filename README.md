# PyOBD - BYMA Market Data Library

Biblioteca Python para acceso a datos del mercado argentino vía **BYMA Open Data API**.

Compatible con la API de [pyhomebroker](https://github.com/crapher/pyhomebroker) para facilitar migración y uso conjunto.

## Instalación

```bash
pip install PyOBD
```

Desde GitLab Package Registry:

```bash
pip install PyOBD \
  --index-url https://gitlab.dlnc.duckdns.org/api/v4/projects/st1tch_bl%2Fpyobd/packages/pypi/simple
```

## Uso rápido

```python
from pyobd import BymaData

client = BymaData()

# Cotización actual
quote = client.get_current_quote("GGAL", settlement="48HS")
print(quote)

# Datos históricos (compatible con pyhomebroker)
df = client.get_daily_history(
    symbol="GGAL",
    from_date="2026-01-01",
    to_date="2026-03-01",
)
print(df.head())

# Datos intradiarios (1-minuto)
idf = client.get_intraday_history("GGAL")
print(idf.head())

# Índices
indices = client.get_indices()
print(indices)
```

## Métodos disponibles

(*Nota: algunos nombres antiguos se mantienen con alias deprecados*)

| Método | Descripción |
|--------|-------------|
| `get_market_time()` | Estado y horario del mercado |
| `get_indices()` | Índices bursátiles |
| `get_bluechips()` | Panel acciones líderes (blue chips) |
| `get_general_board()` | Panel acciones general |
| `get_cedears()` | CEDEARs |
| `get_current_quote(symbol, settlement)` | Cotización actual |
| `get_daily_history(symbol, from_date, to_date)` | Datos históricos OHLCV |
| `get_intraday_history(symbol, from_date=None, to_date=None)` | Datos intradiarios OHLCV 1-minuto |
| `get_government_bonds()` | Títulos públicos |
| `get_corporate_bonds()` | Obligaciones negociables |
| `get_short_term_government_bonds()` | Letras (corto plazo) |
| `get_company_info(symbol)` | Información empresa |
| `get_equity_profile(symbol)` | Perfil especie |
| `get_company_management(symbol)` | Directivos |
| `get_company_balance(symbol)` | Balance |

## Migración desde pyhomebroker

Los métodos clave tienen las mismas firmas y estructura de DataFrame para facilitar la conversión:

```python
# pyhomebroker (requiere cuenta broker)
import pyhomebroker as hb
hb.auth.login(dni=..., user=..., password=..., broker=...)

# Histórico diario
df = hb.history.get_daily_history("GGAL", "2026-01-01", "2026-03-01")
print(df.columns)  # ['date', 'open', 'high', 'low', 'close', 'volume']

# Intradiario
df = hb.history.get_intraday_history("GGAL")

# PyOBD (sin autenticación):
from pyobd import BymaData
client = BymaData()

df = client.get_daily_history("GGAL", "2026-01-01", "2026-03-01")
print(df.columns)  # ['date', 'open', 'high', 'low', 'close', 'volume']

df = client.get_intraday_history("GGAL")
```

Las diferencias menores:

* PyOBD expone los métodos directamente en el cliente (`client.get_*()`)
  en lugar de módulos anidados (`hb.history.*`).
* No se requiere login ni credenciales.
* Algunos nombres de métodos han cambiado (`get_bluechips` vs `get_leading_equity`, etc.) pero existen alias deprecados.

## Licencia

MIT
