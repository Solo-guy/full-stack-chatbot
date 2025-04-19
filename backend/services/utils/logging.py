import logging
import requests
from datetime import datetime

ELK_URL = "http://localhost:9200"

def setup_logging():
    """
    Setup logging to ELK Stack.
    """
    logger = logging.getLogger("admin_system")
    logger.setLevel(logging.INFO)

    class ELKHandler(logging.Handler):
        def emit(self, record):
            try:
                log_entry = {
                    "timestamp": datetime.now().isoformat(),
                    "level": record.levelname,
                    "message": record.getMessage()
                }
                requests.post(f"{ELK_URL}/logs/_doc", json=log_entry)
            except Exception:
                pass

    logger.addHandler(ELKHandler())
    return logger