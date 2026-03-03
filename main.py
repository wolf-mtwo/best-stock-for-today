import argparse
import sys
from src.config import config
from src.utils.logger import setup_logger

# Extractors
from src.extractors.yahoo import YahooExtractor

# Exporters
from src.exporters.excel import ExcelExporter
from src.exporters.json import JsonExporter

logger = setup_logger("main")

def get_extractor(module_name: str):
    if module_name == "yahoo":
        return YahooExtractor()
    else:
        raise ValueError(f"Módulo '{module_name}' no está soportado.")

def get_exporter(format_type: str):
    if format_type == "excel":
        return ExcelExporter()
    elif format_type == "json":
        return JsonExporter()
    else:
        raise ValueError(f"Formato '{format_type}' no está soportado.")

def main():
    parser = argparse.ArgumentParser(description="Extracción de datos del mercado.")
    parser.add_argument(
        "--module", 
        type=str, 
        required=True, 
        choices=config.ALLOWED_MODULES,
        help="El módulo del cual extraer datos (ej. 'yahoo')"
    )
    
    parser.add_argument(
        "--format", 
        type=str, 
        default="excel", 
        choices=config.ALLOWED_FORMATS,
        help="El formato en el cual exportar los datos (ej. 'excel', 'json')"
    )

    parser.add_argument(
        "--include-details", 
        action="store_true", 
        help="Determina si posterior a la tabla resumen se quiere ir a cada empresa para obtener detalles."
    )

    args = parser.parse_args()

    try:
        # 1. Obtención de instancías orquestadas
        extractor = get_extractor(args.module)
        exporter = get_exporter(args.format)
        
        # 2. Extracción (Liskov Substitution Principle / Dependency Inversion Principle)
        logger.info(f"Iniciando flujo de extracción para el módulo '{args.module}' con destino en '{args.format}'")
        data = extractor.extract()
        
        # 3. Exportación
        if data:
            file_path = exporter.export(data, args.module)
            logger.info(f"Proceso finalizado exitosamente. Archivo: {file_path}")
            
            # 4. Extracción Detallada opcional
            if getattr(args, 'include_details', False):
                logger.info("Iniciando extracción detallada por empresa...")
                # Extraer lista de símbolos del listado original
                symbols = [item.symbol for item in data]
                details_data = extractor.extract_all_details(symbols)
                
                if details_data:
                    # Sobrescribimos temporalmente el subdirectorio para diferenciar
                    details_file_path = exporter.export(details_data, f"{args.module}_details")
                    logger.info(f"Proceso de detalles finalizado. Archivo: {details_file_path}")
                else:
                    logger.warning("No se pudo obtener la información detallada.")
                    
        else:
            logger.warning("No se obtuvieron datos. No se exportará ningún archivo.")
            
    except Exception as e:
        logger.error(f"Falla crítica en la ejecución del flujo: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
