import requests
from typing import Optional, Dict
from src.exceptions import NetworkError

class HttpClient:
    """
    Cliente HTTP Dedicado para peticiones del Scraper.
    Aplica principio SRP separando esta lógica del parseo HTML.
    """
    
    def __init__(self, headers: Optional[Dict[str, str]] = None, timeout: int = 15):
        self.headers = headers or {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get_html(self, url: str) -> str:
        """
        Descarga el HTML de la URL especificada manejando comprobaciones estandarizadas.
        
        Args:
            url (str): Target URL para descargar.
            
        Returns:
            str: Contenido HTML recuperado.
            
        Raises:
            NetworkError: Si ocurre un problema descargando o resolviendo el server status.
        """
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.exceptions.HTTPError as he:
            raise NetworkError(f"HTTP Error {he.response.status_code} on {url}: {he}")
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Protocol Error fetching {url}: {e}")
