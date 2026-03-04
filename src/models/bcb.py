from dataclasses import dataclass
from typing import Optional

@dataclass
class BcbData:
    tipo_cambio_oficial_compra: str
    tipo_cambio_oficial_venta: str
    tipo_cambio_oficial_fecha: str
    
    tipo_cambio_referencial_compra: str
    tipo_cambio_referencial_venta: str
    tipo_cambio_referencial_fecha: str
    
    ufv: str
    ufv_fecha: str
    
    oro_internacional: str
    oro_internacional_fecha: str
