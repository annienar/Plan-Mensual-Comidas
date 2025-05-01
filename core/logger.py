"""
Módulo de logging centralizado.

Configura y proporciona funciones de logging consistentes.
"""

import logging
import os
from datetime import datetime
from typing import cast

from core.config import ENCODING_DEFAULT, LOG_DIR, LOGGING_CONFIG


def configurar_logger(nombre: str, nivel: int = logging.INFO) -> logging.Logger:
    """
    Configura un logger con formato estandarizado.

    Args:
        nombre: Nombre del logger
        nivel: Nivel de logging (default: INFO)

    Returns:
        logging.Logger: Logger configurado
    """
    logger = logging.getLogger(nombre)
    logger.setLevel(nivel)

    # Solo configurar si no tiene handlers
    if not logger.handlers:
        # Configurar handler de consola
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(
            logging.Formatter(
                fmt=cast(str, LOGGING_CONFIG["format"]),
                datefmt=cast(str, LOGGING_CONFIG["datefmt"]),
            )
        )
        logger.addHandler(console_handler)

        # Configurar handler de archivo
        if not LOG_DIR.exists():
            os.makedirs(LOG_DIR, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = LOG_DIR / f"log-{timestamp}-{nombre}.txt"

        file_handler = logging.FileHandler(
            log_file,
            encoding=ENCODING_DEFAULT,
        )
        file_handler.setFormatter(
            logging.Formatter(
                fmt=cast(str, LOGGING_CONFIG["format"]),
                datefmt=cast(str, LOGGING_CONFIG["datefmt"]),
            )
        )
        logger.addHandler(file_handler)

        # Silenciar loggers ruidosos
        for noisy_logger in LOGGING_CONFIG["noisy_loggers"]:
            logging.getLogger(noisy_logger).setLevel(logging.WARNING)

    return logger


def log_info(mensaje: str) -> None:
    """Registra un mensaje de nivel INFO."""
    logging.getLogger().info(mensaje)


def log_warning(mensaje: str) -> None:
    """Registra un mensaje de nivel WARNING."""
    logging.getLogger().warning(mensaje)


def log_error(mensaje: str) -> None:
    """Registra un mensaje de nivel ERROR."""
    logging.getLogger().error(mensaje)
