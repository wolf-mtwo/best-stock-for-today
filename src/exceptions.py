class ScrapingBaseError(Exception):
    """Excepción base para el módulo de scraping financiero."""
    pass

class ExtractionError(ScrapingBaseError):
    """Excepción levantada cuando existe un error en la fase de extracción de datos."""
    pass

class ExportError(ScrapingBaseError):
    """Excepción levantada cuando existe un error exportando los datos."""
    pass

class NetworkError(ScrapingBaseError):
    """Excepción levantada cuando la petición HTTP fracasa."""
    pass
