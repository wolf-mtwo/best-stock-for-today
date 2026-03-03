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
