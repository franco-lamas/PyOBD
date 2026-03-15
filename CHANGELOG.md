# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.3.0] - 2026-03-15

### Agregado
- Refactorización completa de la librería como paquete Python modular (`pyobd/`)
- Compatibilidad de API con `pyhomebroker` (migración sin cambiar código de usuario)
- Módulo `client.py`: clase `BymaData` como punto de entrada principal
- Módulo `session.py`: manejo de sesión HTTP con cookies automáticas y reintentos
- Módulo `endpoints.py`: constantes de endpoints de la API de BYMA Open Data
- Módulo `exceptions.py`: excepciones específicas (`BymaDataError`, `APIError`, `ValidationError`)
- Soporte para datos históricos diarios (`get_daily_history`) con resoluciones D/W/M
- Soporte para datos históricos intradía (`get_intraday_history`)
- Soporte para información de empresas: perfil, directivos, balances históricos
- Soporte para mercados SENEBI: bonos, letras y obligaciones negociables
- Métodos para noticias y eventos: hechos relevantes, avisos BYMA, boletines
- Pipeline CI/CD con etapas de test, lint, build y deploy
- Suite de tests con `pytest` y cobertura de código
- Formateo de código con `black` y linting con `flake8`
- Devcontainer para desarrollo reproducible
- Sistema de tareas batch (`.tasks/`)
- Scripts de ejemplo y notebook de referencia (`Scrap_byma_data.ipynb`)

### Cambiado
- Arquitectura reescrita desde módulo único (`PyOBD.py`) a paquete estructurado
- Versión de Python requerida elevada a 3.10+
- Dependencia `pandas` actualizada a >=2.0

### Corregido
- Correcciones en Panel General (`get_general_board`)

---

## [0.2.0] - 2024-10-08

### Agregado
- Ignorado de certificado SSL para todas las consultas HTTP

### Cambiado
- Refactorización de código interno
- Panel de futuros removido (Open BYMA dejó de ofrecer esos datos)

### Corregido
- Correcciones en panel de renta fija (bonos corporativos y públicos)
- Múltiples correcciones en ciclos RC (rc1, rc1-fix1, rc1.1, rc2, rc3, rc4, rc5)

---

## [0.1.9] - 2024-08-07

### Corregido
- Corrección en requerimientos (`requirements.txt`)
- Corrección en panel de bonos corporativos
- Parche en plazos de mercado

---

## [0.1.8] - 2023-11-09

### Corregido
- Correcciones menores generales

---

## [0.1.7] - 2022-06-02

### Agregado
- Campo `close` (precio de cierre) en paneles de datos
- Actualización de bonos IAMC

---

## [0.1.6] - 2022-04-08

### Corregido
- Corrección en panel de CEDEARs

---

## [0.1.5] - 2022-03-03

### Agregado
- Lanzamiento inicial, primera versión funcional
- Consulta de paneles: acciones líderes, panel general, CEDEARs
- Consulta de renta fija: títulos públicos, obligaciones negociables, letras
- Noticias BYMA (`get_byma_news`)
- Indices (`get_indices`)
