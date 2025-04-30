"""
Módulo de logging centralizado.

Configura y proporciona funciones de logging consistentes.
"""

import logging


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
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter(
                fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        logger.addHandler(handler)

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
