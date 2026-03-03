from abc import ABC, abstractmethod
from typing import List, Any
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class BaseExporter(ABC):
    """
    Clase base para todos los exportadores (SOLID: Open/Closed Principle)
    """
    
    def __init__(self):
        self.logger = logger
        
    @abstractmethod
    def export(self, data: List[Any], module_name: str) -> str:
        """
        Método principal de exportación. Debe ser implementado por clases hijas.
        Retorna la ruta absoluta del archivo generado.
        """
        pass
