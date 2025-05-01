# tests/test_normalizador_recetas.py
"""
Tests de integración para el proceso completo de normalización de recetas.

Verifica el flujo completo desde la extracción del texto hasta la
normalización final, para todos los formatos soportados.
"""

import glob
import os
from pathlib import Path
from typing import Any, Dict

import pytest

from core.config import DIR_SIN_PROCESAR
from core.extraer_ocr import extraer_texto_desde_ocr
from core.extraer_pdf import extraer_texto_desde_pdf
from core.extraer_txt import extraer_texto_desde_txt
from core.normalizador_recetas import normalizar_receta_desde_texto

# Ruta absoluta a la carpeta de recetas reales
RECIPE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "recetas", "sin_procesar")
)

# Recopilar todos los archivos de receta
ALL_FILES = glob.glob(os.path.join(RECIPE_DIR, "*"))

# Mapeo de extensiones a funciones extractoras
EXTRACTORES = {
    ".txt": extraer_texto_desde_txt,
    ".pdf": extraer_texto_desde_pdf,
    ".jpg": extraer_texto_desde_ocr,
    ".jpeg": extraer_texto_desde_ocr,
    ".png": extraer_texto_desde_ocr,
}


def obtener_archivos_recetas() -> list[Path]:
    """Obtiene todos los archivos de receta soportados."""
    archivos = []
    for ext in EXTRACTORES.keys():
        archivos.extend(DIR_SIN_PROCESAR.glob(f"*{ext}"))
    return archivos


ARCHIVOS_RECETAS = obtener_archivos_recetas()


def test_existen_archivos_recetas():
    """Verifica que hay archivos de receta para procesar."""
    assert (
        ARCHIVOS_RECETAS
    ), f"No se encontraron archivos de receta en {DIR_SIN_PROCESAR}"


@pytest.mark.parametrize("path_archivo", ARCHIVOS_RECETAS)
def test_extraccion_texto(path_archivo):
    """Verifica la extracción de texto para cada formato."""
    extractor = EXTRACTORES.get(path_archivo.suffix.lower())
    assert extractor, f"No hay extractor para el formato {path_archivo.suffix}"

    texto = extractor(path_archivo)
    assert isinstance(
        texto, str
    ), f"Extractor no devolvió string para {path_archivo.name}"
    assert texto.strip(), f"Extractor devolvió texto vacío para {path_archivo.name}"


@pytest.mark.parametrize("path_archivo", ARCHIVOS_RECETAS)
def test_normalizacion_receta(path_archivo):
    """Verifica la normalización completa de la receta."""
    # Extraer texto según formato
    extractor = EXTRACTORES.get(path_archivo.suffix.lower())
    texto = extractor(path_archivo)

    # Normalizar receta
    receta = normalizar_receta_desde_texto(texto)

    # Validaciones básicas de estructura
    assert isinstance(
        receta, dict
    ), f"Normalización no devolvió dict para {path_archivo.name}"

    # Validar campos requeridos y tipos
    validaciones = {
        "nombre": (str, lambda x: bool(x.strip())),
        "url_origen": (
            str,
            lambda x: x == "Desconocido" or x.startswith(("http://", "https://")),
        ),
        "porciones": (
            (int, str),
            lambda x: x == "Desconocido" or (isinstance(x, int) and 1 <= x <= 20),
        ),
        "calorias_totales": (
            (int, str),
            lambda x: x == "Desconocido" or (isinstance(x, int) and 0 <= x <= 5000),
        ),
        "ingredientes": (list, lambda x: len(x) > 0),
        "preparacion": (list, lambda x: len(x) > 0),
    }

    for campo, (tipo, validador) in validaciones.items():
        # Verificar presencia y tipo
        assert campo in receta, f"Falta campo {campo} en {path_archivo.name}"
        assert isinstance(
            receta[campo], tipo
        ), f"Campo {campo} tiene tipo incorrecto en {path_archivo.name}"

        # Verificar validación específica
        assert validador(
            receta[campo]
        ), f"Validación fallida para {campo} en {path_archivo.name}"


@pytest.mark.parametrize("path_archivo", ARCHIVOS_RECETAS)
def test_consistencia_ingredientes(path_archivo):
    """Verifica la consistencia en el formato de ingredientes."""
    extractor = EXTRACTORES.get(path_archivo.suffix.lower())
    texto = extractor(path_archivo)
    receta = normalizar_receta_desde_texto(texto)

    for ing in receta["ingredientes"]:
        # Verificar estructura
        assert isinstance(ing, dict), f"Ingrediente no es dict en {path_archivo.name}"
        assert all(
            k in ing for k in ["cantidad", "unidad", "nombre"]
        ), f"Faltan campos en ingrediente de {path_archivo.name}"

        # Verificar tipos y rangos
        assert isinstance(
            ing["cantidad"], (int, float)
        ), f"Cantidad no es numérica en {path_archivo.name}"
        assert isinstance(
            ing["unidad"], str
        ), f"Unidad no es string en {path_archivo.name}"
        assert (
            isinstance(ing["nombre"], str) and ing["nombre"].strip()
        ), f"Nombre de ingrediente inválido en {path_archivo.name}"


@pytest.mark.parametrize("path_archivo", ARCHIVOS_RECETAS)
def test_consistencia_preparacion(path_archivo):
    """Verifica la consistencia en los pasos de preparación."""
    extractor = EXTRACTORES.get(path_archivo.suffix.lower())
    texto = extractor(path_archivo)
    receta = normalizar_receta_desde_texto(texto)

    for i, paso in enumerate(receta["preparacion"], 1):
        assert isinstance(paso, str), f"Paso {i} no es string en {path_archivo.name}"
        assert paso.strip(), f"Paso {i} está vacío en {path_archivo.name}"
        assert (
            paso == paso.strip()
        ), f"Paso {i} tiene espacios extra en {path_archivo.name}"
        assert len(paso) <= 500, f"Paso {i} es demasiado largo en {path_archivo.name}"
