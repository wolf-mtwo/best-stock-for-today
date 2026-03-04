# Memoria y Contexto del Proyecto de Extracción de Datos
**Fecha de inicio**: 2026-03-03

## Decisiones Arquitectónicas (SOLID)
- El proyecto utiliza programación orientada a objetos (POO).
- **Single Responsibility Principle (SRP)**: Cada módulo (extractor, exporter, configurador, logger) tiene una única responsabilidad.
- **Open/Closed Principle (OCP)**: Las clases bases de extractores (`src/extractors/base.py`) y exportadores (`src/exporters/base.py`) permiten añadir nuevos orígenes de datos y nuevos formatos de salida sin modificar el código existente.
- **Liskov Substitution Principle (LSP)**: Cualquier clase que herede de un extractor base (`BaseExtractor`) podrá ser usada intercambiablemente.
- **Dependency Inversion Principle (DIP)**: El orquestador principal (`main.py`) dependerá de abstracciones (interfaces de extracción y exportación) y no de implementaciones concretas.

## Estructura del Proyecto
- `/src/models`: Data Classes para tipar los datos extraídos fuertemente.
- `/src/extractors`: Lógica de recolección de datos (ej. requests + BeautifulSoup para Yahoo).
- `/src/exporters`: Lógica para volcar datos a persistencia (ej. Excel usando Pandas, JSON).
- `/src/utils`: Componentes utilitarios transaccionales genéricos (Logging).
- `/src/config.py`: Gestor central de configuración a través del archivo `.env`.

## Extractores Implementados
1. **Yahoo Trending Stocks (`yahoo`)**
   - URL: `https://finance.yahoo.com/markets/stocks/trending/`
   - **Nivel 1 (Resumen)**: Extrae 10 campos `symbol`, `name`, `price`, `change`, `change_percent`, `volume`, `avg_vol_3m`, `market_cap`, `pe_ratio_ttm`, `week_52_change_percent`.
   - **Nivel 2 (Detalles)**: Navega a cada subpágina (ej: `https://finance.yahoo.com/quote/{symbol}`) para extraer 16 campos extendidos tales como `previous_close`, `open_price`, y los valores primarios `current_price`, `numeric_change`, y `percentage_change` (obtenidos de la clase de cabecera en tiempo real de Yahoo).
2. **Banco Central de Bolivia (`bcb`)**
   - URL: `https://www.bcb.gob.bo/`
   - Navega al DOM central del Banco para parsear datos volátiles incluyendo `tipo_cambio_oficial`, `tipo_cambio_referencial`, `ufv` y la cotización del `oro_internacional`.


## Exportadores Implementados
1. **Excel** (`excel`)
   - Guarda los DataFrames de forma estructurada en `/datos/{modulo}/{fecha_actual}/<hora>.xlsx`
2. **JSON** (`json`)
   - Guarda una estructura JSON en `/datos/{modulo}/{fecha_actual}/<hora>.json`
