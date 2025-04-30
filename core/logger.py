"""
Logger central del proyecto Plan Mensual de Comidas
---------------------------------------------------
• Un archivo por módulo  → .log/<versión>/log-<mm-dd-HHMM>-<módulo>.txt
• Mensajes visibles en consola *sin* duplicarse.
• La cabecera de versión se escribe solo en el archivo (nivel DEBUG),
  de modo que nunca “ensucia” la salida en pantalla.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from pathlib import Path

# Ruta raíz para logs
LOG_ROOT = Path(os.path.abspath(os.path.dirname(__file__))) / '..' / '.log'
LOG_ROOT = LOG_ROOT.expanduser().resolve()
LOG_ROOT.mkdir(parents=True, exist_ok=True)

# Formato y datefmt
_FMT = "%(asctime)s - %(levelname)s - %(message)s"
_DATEFMT = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(_FMT, datefmt=_DATEFMT)


def configurar_logger(nombre_modulo: str) -> logging.Logger:
    """
    Configura (una sola vez) el logger raíz y devuelve la misma
    instancia para cualquier módulo que la solicite.
    """
    root = logging.getLogger()

    # Si ya hay handlers, devolvemos la instancia existente
    if root.handlers:
        return root

    root.setLevel(logging.DEBUG)

    # ---------- FileHandler -------------------------------------------------
    ts = datetime.now().strftime("log-%m-%d-%H%M")
    log_path = LOG_ROOT / f"{ts}-{nombre_modulo}.txt"
    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    root.addHandler(fh)

    # ---------- ConsoleHandler ----------------------------------------------
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    root.addHandler(ch)

    # Reducir verbosity de librerías de terceros
    for noisy in ("pdfminer", "pdfplumber", "PIL"):
        logging.getLogger(noisy).setLevel(logging.ERROR)

    return root


# ------------------------------------------------------------------ #
# Wrappers “one-liner”                                               #
# Llaman directamente al logger raíz y no crean handlers duplicados. #
# ------------------------------------------------------------------ #
def log_info(msg: str) -> None:
    logging.getLogger().info(msg)

def log_warning(msg: str) -> None:
    logging.getLogger().warning(msg)

def log_error(msg: str) -> None:
    logging.getLogger().error(msg)
