import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Base paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "datos")
    
    # Módulos permitidos
    ALLOWED_MODULES = ["yahoo", "bcb"]
    ALLOWED_FORMATS = ["excel", "json"]

config = Config()
