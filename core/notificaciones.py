"""
Módulo de notificaciones y mensajes de log estandarizados.

Proporciona funciones wrapper para logging con formatos consistentes.
"""

from pathlib import Path
from typing import List, Union

from core.logger import log_error, log_info, log_warning

PathLike = Union[str, Path]


def log_creacion_carpeta(path: PathLike) -> None:
    """Notifica la creación de una carpeta."""
    log_info(f"📁 Creada carpeta: {path}")


def log_movimiento_archivo(origen: PathLike, destino: PathLike) -> None:
    """Notifica el movimiento de un archivo."""
    log_info(f"📄 Movido: {origen} → {destino}")


def log_creacion_archivo(path: PathLike) -> None:
    """Notifica la creación de un archivo."""
    log_info(f"📄 Creado: {path}")


def log_receta_normalizada(nombre: str) -> None:
    """Notifica la normalización exitosa de una receta."""
    log_info(f"✅ Receta normalizada: {nombre}")


def log_error_archivo(path: PathLike, mensaje: str) -> None:
    """Notifica un error al procesar un archivo."""
    log_error(f"❌ Error en {path}: {mensaje}")


def log_fuentes_encontradas(nombre: str, cantidad: int) -> None:
    """Notifica las fuentes encontradas en una receta."""
    log_info(f"📚 Receta '{nombre}': {cantidad} fuentes encontradas")


def log_metadatos_incompletos(nombre: str, faltantes: List[str]) -> None:
    """Notifica metadatos faltantes en una receta."""
    log_warning(f"⚠️ Receta '{nombre}': Faltan metadatos: {', '.join(faltantes)}")


def log_error_parseo(nombre: str, etapa: str, error: str) -> None:
    """Notifica un error durante el parseo de una receta."""
    log_error(f"❌ Error al parsear '{nombre}' en {etapa}: {error}")


def log_codificacion_invalida(path: PathLike) -> None:
    """Notifica un error de codificación en un archivo."""
    log_error(f"❌ Codificación inválida en {path}")


def log_formato_invalido(path: PathLike, razon: str) -> None:
    """Notifica un formato de archivo inválido."""
    log_error(f"❌ Formato inválido en {path}: {razon}")


def log_carpeta_vacia(path: PathLike) -> None:
    """Notifica que una carpeta está vacía."""
    log_info(f"📂 No hay archivos para procesar en {path}")
