import logging
from bs4 import BeautifulSoup
from typing import List, Any
from src.extractors.base import BaseExtractor
from src.models.stock import StockData, CompanyDetails
from src.exceptions import ExtractionError, NetworkError
from src.utils.http_client import HttpClient

class YahooExtractor(BaseExtractor):
    """
    Extractor para Yahoo Finance Trending Stocks utilizando BeautifulSoup.
    Cumple con el OCP al extender BaseExtractor y respeta el SRP al delegar peticiones a self.http_client.
    """
    
    URL = "https://finance.yahoo.com/markets/stocks/trending/"
    
    def __init__(self, logger: logging.Logger, http_client: HttpClient):
        """
        Constructor con inyección de dependencias.
        Args:
            logger (logging.Logger): Transmite logs hacia las consolas.
            http_client (HttpClient): Realiza peticiones web y recupera HTML.
        """
        super().__init__(module_name="yahoo", logger=logger, http_client=http_client)
        
    def extract(self) -> List[StockData]:
        self.logger.info(f"[{self.module_name}] Iniciando extracción desde {self.URL}")
        
        try:
            html_content = self.http_client.get_html(self.URL)
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Buscar la tabla - se ajusta al HTML provisto
            table = soup.find('table', class_='yf-1tpeyy7')
            if not table:
                self.logger.warning(f"[{self.module_name}] No se encontró la tabla en el HTML.")
                return []
                
            tbody = table.find('tbody')
            if not tbody:
                self.logger.warning(f"[{self.module_name}] No se encontró el tbody en la tabla.")
                return []
                
            rows = tbody.find_all('tr', class_='row')
            self.logger.info(f"[{self.module_name}] Se encontraron {len(rows)} filas.")
            
            data_list = []
            
            for index, row in enumerate(rows):
                try:
                    cells = row.find_all('td')
                    if len(cells) < 11:
                        continue
                        
                    # Extraer base en la posición del HTML
                    # 0: Symbol
                    # 1: Name
                    # 2: Sparkline (Ignorar)
                    # 3: Price
                    # 4: Change
                    # 5: Change %
                    # 6: Volume
                    # 7: Avg Vol (3M)
                    # 8: Market Cap
                    # 9: P/E Ratio
                    # 10: 52 Wk Change %
                    
                    symbol = cells[0].find(class_='symbol').text.strip() if cells[0].find(class_='symbol') else ""
                    name = cells[1].text.strip()
                    
                    # Precio: en div class="" -> span
                    price_span = cells[3].find('span')
                    price = float(price_span.text.strip().replace(',', '')) if price_span else 0.0
                    
                    change = cells[4].text.strip()
                    change_percent = cells[5].text.strip()
                    volume = cells[6].text.strip()
                    avg_vol_3m = cells[7].text.strip()
                    market_cap = cells[8].text.strip()
                    pe_ratio_ttm = cells[9].text.strip()
                    week_52_change_percent = cells[10].text.strip()
                    
                    stock = StockData(
                        symbol=symbol,
                        name=name,
                        price=price,
                        change=float(change.replace(',', '')) if change and change != '--' else 0.0,
                        change_percent=change_percent,
                        volume=volume,
                        avg_vol_3m=avg_vol_3m,
                        market_cap=market_cap,
                        pe_ratio_ttm=pe_ratio_ttm,
                        week_52_change_percent=week_52_change_percent
                    )
                    
                    data_list.append(stock)
                    
                except Exception as e:
                    self.logger.error(f"[{self.module_name}] Error parseando la fila {index}: {e}")
                    continue
                    
            self.logger.info(f"[{self.module_name}] Extracción finalizada. Registros procesados: {len(data_list)}")
            return data_list
            
        except NetworkError as ne:
            self.logger.error(f"[{self.module_name}] Error de red durante la extracción: {ne}")
            raise ExtractionError(str(ne))
        except Exception as e:
            self.logger.error(f"[{self.module_name}] Error general: {e}")
            raise ExtractionError(str(e))

    def extract_details(self, symbol: str) -> CompanyDetails:
        url = f"https://finance.yahoo.com/quote/{symbol}/"
        self.logger.info(f"[{self.module_name}] Extrayendo detalles de {symbol} en {url}")
        
        try:
            html_content = self.http_client.get_html(url)
            soup = BeautifulSoup(html_content, 'html.parser')
            ul_element = soup.find('ul', class_='yf-6myrf1')
            
            if not ul_element:
                self.logger.warning(f"[{self.module_name}] No se encontró la lista de detalles para {symbol}.")
                return None
                
            items = ul_element.find_all('li')
            
            # Helper para buscar por título (label)
            def get_value_by_title(title: str) -> str:
                for item in items:
                    label_span = item.find('span', class_='label')
                    if label_span and title.lower() in label_span.text.lower():
                        val_span = item.find('span', class_='value')
                        return val_span.text.strip() if val_span else ""
                return ""
            
            details = CompanyDetails(
                symbol=symbol,
                previous_close=get_value_by_title("Previous Close"),
                open_price=get_value_by_title("Open"),
                bid=get_value_by_title("Bid"),
                ask=get_value_by_title("Ask"),
                days_range=get_value_by_title("Day's Range"),
                week_52_range=get_value_by_title("52 Week Range"),
                volume=get_value_by_title("Volume"),
                avg_volume=get_value_by_title("Avg. Volume"),
                market_cap=get_value_by_title("Market Cap (intraday)"),
                beta_5y=get_value_by_title("Beta (5Y Monthly)"),
                pe_ratio_ttm=get_value_by_title("PE Ratio (TTM)"),
                eps_ttm=get_value_by_title("EPS (TTM)"),
                earnings_date=get_value_by_title("Earnings Date"),
                forward_dividend_yield=get_value_by_title("Forward Dividend & Yield"),
                ex_dividend_date=get_value_by_title("Ex-Dividend Date"),
                target_est_1y=get_value_by_title("1y Target Est")
            )
            
            return details
            
        except Exception as e:
            self.logger.error(f"[{self.module_name}] Error obteniendo detalles para {symbol}: {e}")
            return None
