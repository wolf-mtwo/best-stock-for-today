import os
import json
import datetime
from dataclasses import asdict
from typing import List, Any
import logging
from src.exceptions import ExportError
from src.exporters.base import BaseExporter

class JsonExporter(BaseExporter):
    """
    Exportador de datos en formato JSON.
    Aplica principio SRP delegando configuración a inyección de dependencias.
    """
    
    def __init__(self, logger: logging.Logger, output_dir: str):
        super().__init__(logger=logger, output_dir=output_dir)
    
    def export(self, data: List[Any], module_name: str) -> str:
        if not data:
            self.logger.warning(f"[{module_name}] No hay datos para exportar a JSON.")
            return ""
            
        try:
            # Convertir dataclasses a diccionarios
            dict_data = [asdict(item) if hasattr(item, "__dataclass_fields__") else item for item in data]
            
            # Generar estructura de carpetas: datos/<module>/<date>/
            now = datetime.datetime.now()
            date_str = now.strftime("%Y-%m-%d")
            time_str = now.strftime("%H%M%S")
            
            folder_path = os.path.join(self.output_dir, module_name, date_str)
            os.makedirs(folder_path, exist_ok=True)
            
            file_name = f"{time_str}.json"
            file_path = os.path.join(folder_path, file_name)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(dict_data, f, ensure_ascii=False, indent=4)
                
            self.logger.info(f"[{module_name}] Datos exportados exitosamente a {file_path}")
            
            return file_path
            
        except Exception as e:
            self.logger.error(f"Error al exportar a JSON: {e}")
            raise ExportError(f"Falló guardando archivo JSON: {e}")
