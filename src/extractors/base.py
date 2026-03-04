from abc import ABC, abstractmethod
from typing import List, Any
import logging
from src.utils.http_client import HttpClient

class BaseExtractor(ABC):
    """
    Clase base para todos los extractores.
    Se inyectan dependencias como el logger y el http_client (SOLID: DIP)
    """
    
    def __init__(self, module_name: str, logger: logging.Logger, http_client: HttpClient):
        """
        Inicializa un extrator genérico.
        Args:
            module_name (str): Selector del módulo de base de datos.
            logger (logging.Logger): Dependencia inyectada para registros.
            http_client (HttpClient): Dependencia inyectada para efectuar peticiones web.
        """
        self.module_name = module_name
        self.logger = logger
        self.http_client = http_client
        
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
