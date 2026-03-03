from abc import ABC, abstractmethod
from typing import List, Any
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class BaseExtractor(ABC):
    """
    Clase base para todos los extractores (SOLID: Open/Closed Principle)
    """
    
    def __init__(self, module_name: str):
        self.module_name = module_name
        self.logger = logger
        
    @abstractmethod
    def extract(self) -> List[Any]:
        """
        Método principal de extracción. Debe ser implementado por clases hijas.
        """
        pass
        
    @abstractmethod
    def extract_details(self, symbol: str) -> Any:
        """
        Extrae datos profundos/detallados de un símbolo específico.
        """
        pass
        
    def extract_all_details(self, symbols: List[str]) -> List[Any]:
        """
        Extrae detalles de una lista de símbolos.
        """
        details = []
        for sym in symbols:
            try:
                detail = self.extract_details(sym)
                if detail:
                    details.append(detail)
            except Exception as e:
                self.logger.error(f"Error extrayendo detalles globales para {sym}: {e}")
        return details
