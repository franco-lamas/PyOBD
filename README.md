# PyOBD
## Overview
PyOBD es una API para conectar cualquier script de Python con datos del mercado con 20 minutos de retraso provistos por Open BYMA Data, además permite la descarga de datos histórico. Fue desarrollada en conjunto por [Nacho Herrera](https://github.com/nacho-herrera), [St1tch](https://twitter.com/St1tch_BL) y [Franco Lamas](https://www.linkedin.com/in/franco-lamas/).

# Uso
## Inicialización
    from PyOBD import *
    PyOBD=openBYMAdata()

## Datos de mercados

Por el momento solo se encuentra disponible el plazo de 48hs que viene cargado por defecto

### Cotizaciones de Bonos

    PyOBD.get_bonds()

### Cotizaciones de Letras

    PyOBD.get_short_term_bonds()

### Cotizaciones de Bonos Coporativos
    PyOBD.get_corporateBonds()

### Cotizaciones del Panel MERVAL

    PyOBD.get_bluechips()

### Cotizaciones del Panel General

    PyOBD.get_galpones()

### Cotizaciones de CEDEAR

    PyOBD.get_cedears()

### Cotizaciones de los índices 

    PyOBD.indices()
    
### Cotizaciones de opciones

    PyOBD.get_options()

## Llamadas generales
### Noticias

    PyOBD.byma_news()

### Dia laborable (boolean) 

    PyOBD.isworkingDay()

### Resumen de mercado 

    PyOBD.marketResume()

# Instalacion

La instalación vía pip aún no está disponible, únicamente desde el repositorio. Se requiere instalar [Git](https://git-scm.com/).

    pip install git+https://github.com/franco-lamas/PyOBD --upgrade --no-cache-dir


# Problemas Conocidos
*   Luego de las 2am se reinicia el servidor y cambia la estructura de datos.
*   Luego de las 17 la sección de noticias se desconecta.

# To-do list


*   Agregar más plazos
*   Formatear links de noticias
*   Dashboard de bonos IAMC
*   Datos de empresas
*   Históricos
*   Balances históricos


# DISCLAIMER

La información es mostrada “tal cual es”, puede ser incorrecta o contener errores, eso es responsabilidad de cada sitio. No somos responsables por el uso indebido de los Scripts.
