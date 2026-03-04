import logging
import re
from typing import List, Any
from bs4 import BeautifulSoup

from src.extractors.base import BaseExtractor
from src.utils.http_client import HttpClient
from src.exceptions import ExtractionError, NetworkError
from src.models.bcb import BcbData

class BcbExtractor(BaseExtractor):
    """
    Extractor para datos macroeconómicos del Banco Central de Bolivia (BCB).
    Cumple con el OCP al extender BaseExtractor y respeta el SRP al delegar peticiones al cliente HTTP inyectado.
    """
    
    URL = "https://www.bcb.gob.bo/"
    
    def __init__(self, logger: logging.Logger, http_client: HttpClient):
        """
        Constructor con inyección de dependencias.
        Args:
            logger (logging.Logger): Transmite logs hacia las consolas.
            http_client (HttpClient): Realiza peticiones web y recupera HTML.
        """
        super().__init__(module_name="bcb", logger=logger, http_client=http_client)
        # Deshabilitamos la verificación SSL transitoriamente para BCB dado que presenta issues reportados
        self.http_client.session.verify = False
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
    def extract(self) -> List[BcbData]:
        self.logger.info(f"[{self.module_name}] Iniciando extracción desde {self.URL}")
        
        try:
            html_content = self.http_client.get_html(self.URL)
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Utilizar localizadores robustos en base al DOM provisto
            
            def safe_extract_text(sibling_elem) -> str:
                return sibling_elem.text.strip().replace('\n', ' ') if sibling_elem else ""

            # 1. Tipo de cambio oficial
            # Localizamos la sección por el título
            oficial_block = soup.find(lambda tag: tag.name == "div" and "TIPO DE CAMBIO" in tag.text)
            tc_oficial_fecha = ""
            tc_oficial_compra = ""
            tc_oficial_venta = ""
            
            if oficial_block:
                texto_limpio = oficial_block.text.replace('\n', ' ')
                # Extraer Fecha (ej. martes 3 de marzo, 2026)
                m_fecha = re.search(r'(lunes|martes|miércoles|jueves|viernes|sábado|domingo)\s+\d+\s+de\s+[a-z]+,\s+\d{4}', texto_limpio)
                if m_fecha:
                    tc_oficial_fecha = m_fecha.group(0)
                    
                # Extraer Compra y Venta
                m_compra = re.search(r'Compra:\s*([\d,]+)', texto_limpio)
                m_venta = re.search(r'Venta:\s*([\d,]+)', texto_limpio)
                if m_compra: tc_oficial_compra = m_compra.group(1)
                if m_venta: tc_oficial_venta = m_venta.group(1)

            # 2. Tipo de cambio referencial
            ref_block = soup.find(lambda tag: tag.name == "div" and "VALOR REFERENCIAL DEL DÓLAR ESTADOUNIDENSE" in tag.text)
            tc_ref_fecha = tc_oficial_fecha # Suelen compartir el bloque superior o formato
            tc_ref_compra = ""
            tc_ref_venta = ""
            
            if ref_block:
                texto_limpio = ref_block.text.replace('\n', ' ')
                m_fecha = re.search(r'(lunes|martes|miércoles|jueves|viernes|sábado|domingo)\s+\d+\s+de\s+[a-z]+,\s+\d{4}', texto_limpio)
                if m_fecha: tc_ref_fecha = m_fecha.group(0)
                
                m_compra = re.search(r'Compra:\s*([\d,]+)', texto_limpio)
                m_venta = re.search(r'Venta:\s*([\d,]+)', texto_limpio)
                if m_compra: tc_ref_compra = m_compra.group(1)
                if m_venta: tc_ref_venta = m_venta.group(1)

            # 3. UFV
            ufv_block = soup.find(lambda tag: tag.name == "div" and "UFV" in tag.text and "Bs" in tag.text)
            ufv_fecha = ""
            ufv_valor = ""
            
            if ufv_block and ufv_block.parent:
                texto_limpio = ufv_block.parent.text.replace('\n', ' ').strip()
                # El texto suele ser: "martes 3 de marzo, 2026 Bs3,14517  por UFV"
                m_fecha = re.search(r'(lunes|martes|miércoles|jueves|viernes|sábado|domingo)\s+\d+\s+de\s+[a-z]+,\s+\d{4}', texto_limpio)
                if m_fecha: ufv_fecha = m_fecha.group(0)
                
                m_valor = re.search(r'Bs([0-9.,]+)', texto_limpio)
                if m_valor: ufv_valor = m_valor.group(1)

            # 4. Oro Internacional
            oro_block = soup.find(lambda tag: tag.name == "div" and "COTIZACIÓN INTERNACIONAL DEL ORO" in tag.text)
            oro_fecha = ""
            oro_valor = ""
            
            if oro_block and oro_block.parent:
                texto_limpio = oro_block.parent.text.replace('\n', ' ')
                # Extraemos la fecha del padre
                m_fecha = re.search(r'(lunes|martes|miércoles|jueves|viernes|sábado|domingo)\s+\d+\s+de\s+[a-z]+,\s+\d{4}', texto_limpio)
                if m_fecha: oro_fecha = m_fecha.group(0)
                
                # Extraemos la primer cifra que luzca como miles de dólares. Normalmente "USD 2.650,45"
                m_valor = re.search(r'([Oo]nza.*?[0-9.,]+|[0-9]{1,3}\.[0-9]{3},[0-9]{2})', texto_limpio)
                if m_valor: 
                    oro_valor = m_valor.group(1)
                else:
                    # Fallback agresivo a números con comas/puntos altos (ej 2.054,00)
                    fallback = re.search(r'([1-9]\.[0-9]{3},[0-9]{2})', texto_limpio)
                    if fallback: oro_valor = fallback.group(1)
                    
            data = BcbData(
                tipo_cambio_oficial_compra=tc_oficial_compra,
                tipo_cambio_oficial_venta=tc_oficial_venta,
                tipo_cambio_oficial_fecha=tc_oficial_fecha,
                tipo_cambio_referencial_compra=tc_ref_compra,
                tipo_cambio_referencial_venta=tc_ref_venta,
                tipo_cambio_referencial_fecha=tc_ref_fecha,
                ufv=ufv_valor,
                ufv_fecha=ufv_fecha,
                oro_internacional=oro_valor,
                oro_internacional_fecha=oro_fecha
            )
            
            self.logger.info(f"[{self.module_name}] Extracción BCB finalizada.")
            return [data]
            
        except NetworkError as ne:
            self.logger.error(f"[{self.module_name}] Error de red durante la extracción: {ne}")
            raise ExtractionError(str(ne))
        except Exception as e:
            self.logger.error(f"[{self.module_name}] Error general: {e}")
            raise ExtractionError(str(e))

    def extract_details(self, symbol: str) -> Any:
        # El módulo BCB no posee extracción profunda por el momento, retorna None amablemente (LSP)
        return None
