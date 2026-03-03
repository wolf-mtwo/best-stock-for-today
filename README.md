# Extractor de Datos del Mercado Financiero 📊

Proyecto en Python enfocado en la extracción de datos financieros mediante web scraping (por defecto, enfocado en "Trending Stocks" de Yahoo Finance) con exportación estructurada a Excel o JSON.

## Arquitectura (Principios SOLID)
Este proyecto se desarrolló utilizando Programación Orientada a Objetos (POO).
- **SRP (Single Responsibility)**: Existen componentes separados para carga de config, logging, modelo de datos, extractores y exportadores.
- **OCP (Open/Closed)**: Arquitectura basada en interfaces puras de `BaseExtractor` y `BaseExporter`. Es fácil añadir un nuevo portal a consultar o un nuevo formato a guardar sin alterar el core. 
- **LSP & DIP**: Componentes que usan herencia abstracta, permitiendo polimorfismo desde el `main.py`.

## Estructura de Proyecto
```
best-stock-for-today/
├── datos/                  # Carpeta de guardado (autocreada)
├── src/                    # Fuentes del Proyecto
│   ├── config.py           # Configuración (variables de entorno)
│   ├── utils/
│   │   └── logger.py       # Configuración de log
│   ├── models/
│   │   └── stock.py        # Dominio (Data Classes)
│   ├── extractors/
│   │   ├── base.py         # Interfaces abstracto
│   │   └── yahoo.py        # Estrategia concreta de Yahoo
│   └── exporters/
│       ├── base.py         # Interfaces abstracto
│       ├── excel.py        # Generación de XLSX
│       └── json.py         # Exportación JSON
├── venv/                   # Virtual environment (se genera local)
├── requirements.txt        # Dependencias
├── .env                    # Variables del sistema
└── main.py                 # Orquestador (CLI)
```

## Requisitos
- Python 3.10 o superior
- pip

## Instrucciones de Instalación
1. Clonar este repositorio e ingresar al directorio principal.
   ```bash
   cd /opt/uab/best-stock-for-today
   ```
2. Crear un entorno virtual y activarlo:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Instalar sus dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Configurar el archivo `.env`:
   Modifica o valida el `.env`, por defecto utiliza `LOG_LEVEL=INFO`.

## Ejecución del Sistema
El proceso funciona mediante la línea de comandos e incluye parámetros predefinidos.

**Básico (Generar en Excel):**
Se creará un Excel de la extracción en: `datos/yahoo/YYYY-MM-DD/HHMMSS.xlsx`
```bash
python main.py --module yahoo --format excel
```

**Guardado en JSON:**
Generará una estructura JSON en lugar de usar pandas.
```bash
python main.py --module yahoo --format json
```

**Ver Ayuda del CLI:**
```bash
python main.py --help
```