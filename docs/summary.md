# Resumen Ejecutivo: Proyecto Integrador de Web Scraping

El proyecto se estructuró a través de **4 fases evolutivas**, asegurando el cumplimiento de **principios SOLID y Clean Architecture**, partiendo desde una recolección simple en tabla hasta un ecosistema multiplataforma con delegación de responsabilidades.

---

## Fase 1: Arquitectura Base y Primer Extractor (Yahoo)
En esta fase inicial sentamos los cimientos del ecosistema en Python:
1. **Modelos y Estructuras Fundamentales (SOLID - OCP)**:
   - Se construyeron interfaces abstractas mediante la clase `BaseExtractor` y `BaseExporter`.
   - Implementación de un modelo de datos fuertemente tipado (`StockData`) usando `@dataclass` para estandarizar los indicadores financieros de las acciones (Símbolo, precio, volumen, % de cambio anual, etc).
2. **Generación de Reportes**:
   - Creación de `ExcelExporter` para generar dinámicamente archivos `.xlsx` bajo la jerarquía `datos/<módulo>/<fecha>/<hora>.xlsx`.
   - Creación de `JsonExporter` para alternativas ligeras.
3. **Módulo de Scraping (Yahoo Trending Stocks)**:
   - Se implementó `YahooExtractor` utilizando `BeautifulSoup` para navegar el DOM y extraer de forma programática las entidades de cabecera tabuladas en Yahoo Finance.

## Fase 2: Navegación Profunda (Deep Scraping)
Extendimos la capacidad del extractor para superar recolecciones planas de una sola página.
1. **Generación de Detalles Secundarios (`CompanyDetails`)**:
   - Agregamos 16 campos internos de la vista de cada compañía ("Previous Close", "PE Ratio", "Volume", "Earnings Date", etc.).
2. **Metodología Iterativa**:
   - Al ejecutar mediante el nuevo flag `--include-details`, el sistema compila la lista maestra de acciones y procede a navegar subdirección por subdirección (`https://finance.yahoo.com/quote/{symbol}`) recolectando la metadata oculta.
   - El resultado se deposita paralelamente en carpetas exclusivas (`datos/yahoo_details/..`) garantizando inmunidad a interrupciones.

## Fase 3: Refactorización Estructural (Clean Architecture)
El proyecto se actualizó conforme al entorno productivo industrial para lograr alta disponibilidad y mínima interdependencia (SRP, DIP):
1. **Cliente HTTP Independiente (`HttpClient`)**:
   - Abstrayendo todo uso de librerías como `requests` directamente en el scraper, permitiendo un manejo central de `Timeouts`, configuración de `User-Agents`, control de fallos SSL u homologación de sesiones concurrentes a futuro.
2. **Inyección de Dependencias (Dependency Injection)**:
   - Convertimos a `main.py` en nuestro **Composition Root**. Todos los extractores y exportadores pasaron a exigir y recibir por parámetro sus dependencias absolutas (`Logger`, `HttpClient`, directorio de guardado), aislando su preocupación principal a únicamente funcionar de la manera en que fueron construidos.
3. **Excepciones de Dominio Personalizadas**:
   - Implementación de `ExtractionError`, `NetworkError` y `ExportError` bajo la envoltura `ScrapingBaseError`. El código ya no atrapa "excepciones en blanco", diagnosticando el fallo exacto permitiendo reintentos lógicos sin caídas.

## Fase 4: Mejoras Multimódulo (Incorporación BCB)
Finalizamos el software expandiendo su horizonte modular, sumando la recolección estricta de parámetros macroeconómicos.
1. **Mejoras del Reporte de Yahoo**:
   - Incorporación paralela desde las etiquetas frontales (`fin-streamer`) para obtener los valores precisos en tiempo real: `current_price` (Costo Actual), `numeric_change` (Variación Monetaria), e `percentage_change` (Variación Porcentual).
2. **Extractor de Banco Central de Bolivia (`bcb`)**:
   - Creación del Módulo Institucional `BcbExtractor` acoplado al `HttpClient`.
   - Reglas avanzadas (Regex + BeautifulSoup) buscando patrones DOM específicos para garantizar la obtención veraz del: **Tipo de cambio oficial** (Compra/Venta), **Tipo de cambio referencial** (Compra/Venta), el costo de la **UFV** (Unidad de Fomento de Vivienda) y el **Oro Internacional**.
3. **Integración al CLI Maestro**:
   - Actualización del CLI para soportar comandos pre-configurados. Iniciar la tarea del BCB se orquesta centralizadamente empleando simplemente:
     `python main.py --module bcb --format json`
