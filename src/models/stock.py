from dataclasses import dataclass
from typing import Optional

@dataclass
class StockData:
    symbol: str
    name: str
    price: float
    change: float
    change_percent: str
    volume: str
    avg_vol_3m: str
    market_cap: str
    pe_ratio_ttm: str
    week_52_change_percent: str
