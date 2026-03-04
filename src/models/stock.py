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

@dataclass
class CompanyDetails:
    symbol: str
    current_price: str
    numeric_change: str
    percentage_change: str
    previous_close: str
    open_price: str
    bid: str
    ask: str
    days_range: str
    week_52_range: str
    volume: str
    avg_volume: str
    market_cap: str
    beta_5y: str
    pe_ratio_ttm: str
    eps_ttm: str
    earnings_date: str
    forward_dividend_yield: str
    ex_dividend_date: str
    target_est_1y: str

