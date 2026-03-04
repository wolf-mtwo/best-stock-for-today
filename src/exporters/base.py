from abc import ABC, abstractmethod
from typing import List, Any
import logging

class BaseExporter(ABC):
    """
    Clase base para todos los exportadores.
    Se inyectan dependencias como el logger (SOLID: DIP)
    """
    
    def __init__(self, logger: logging.Logger, output_dir: str):
        """
        Inicializa un exportador genérico.
        Args:
            logger (logging.Logger): Instancia para registrar logs.
            output_dir (str): Directorio raíz donde se exportarán los archivos.
        """
        self.logger = logger
        self.output_dir = output_dir
        
    @abstractmethod
    def export(self, data: List[Any], module_name: str) -> str:
        """
        Método principal de exportación. Debe ser implementado por clases hijas.
        Retorna la ruta absoluta del archivo generado.
        """
        pass
