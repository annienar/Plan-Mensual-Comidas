import logging
import os
from datetime import datetime

def configurar_logger(nombre="script"):
    os.makedirs(".log", exist_ok=True)
    timestamp = datetime.now().strftime("%m-%d-%H%M")
    log_path = f".log/log-{timestamp}-{nombre}.txt"

    logging.basicConfig(
        filename=log_path,
        filemode="w",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )

    return logging.getLogger(nombre)
