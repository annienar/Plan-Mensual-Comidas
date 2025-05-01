"""
Tests para la validación de metadatos de recetas.

Verifica la extracción y validación de metadatos de recetas
independientemente del formato de origen.
"""

from pathlib import Path
from typing import Any, Dict

import pytest

from core.config import DIR_SIN_PROCESAR
from core.metadatos_recetas import (
    extraer_calorias,
    extraer_nombre,
    extraer_porciones,
    extraer_preparacion,
    extraer_url_origen,
    normalizar_receta_desde_texto,
    parsear_ingredientes,
)

# Obtener todos los archivos de receta
ARCHIVOS_RECETAS = list(DIR_SIN_PROCESAR.glob("*.txt"))  # Expandir para más formatos


def test_existen_archivos_recetas():
    """Asegurar que hay archivos de recetas para procesar."""
    assert (
        ARCHIVOS_RECETAS
    ), f"No se encontraron archivos de recetas en {DIR_SIN_PROCESAR}"


@pytest.mark.parametrize("path_archivo", ARCHIVOS_RECETAS)
def test_extraccion_nombre(path_archivo):
    """Verifica la extracción del nombre de la receta."""
    with open(path_archivo, "r", encoding="utf-8") as f:
        texto = f.read()

    nombre = extraer_nombre(texto)
    assert nombre, f"No se pudo extraer nombre de {path_archivo.name}"
    assert nombre != "Desconocido", f"Nombre no detectado en {path_archivo.name}"
    assert (
        len(nombre.splitlines()) == 1
    ), f"Nombre contiene múltiples líneas en {path_archivo.name}"


@pytest.mark.parametrize("path_archivo", ARCHIVOS_RECETAS)
def test_extraccion_url(path_archivo):
    """Verifica la extracción de URL de origen."""
    with open(path_archivo, "r", encoding="utf-8") as f:
        texto = f.read()

    url = extraer_url_origen(texto)
    if url != "Desconocido":
        assert url.startswith(
            ("http://", "https://")
        ), f"URL inválida en {path_archivo.name}"


@pytest.mark.parametrize("path_archivo", ARCHIVOS_RECETAS)
def test_extraccion_porciones(path_archivo):
    """Verifica la extracción del número de porciones."""
    with open(path_archivo, "r", encoding="utf-8") as f:
        texto = f.read()

    porciones = extraer_porciones(texto)
    if isinstance(porciones, int):
        assert (
            1 <= porciones <= 20
        ), f"Número de porciones fuera de rango en {path_archivo.name}"


@pytest.mark.parametrize("path_archivo", ARCHIVOS_RECETAS)
def test_extraccion_calorias(path_archivo):
    """Verifica la extracción de calorías."""
    with open(path_archivo, "r", encoding="utf-8") as f:
        texto = f.read()

    calorias = extraer_calorias(texto)
    if isinstance(calorias, int):
        assert 0 <= calorias <= 5000, f"Calorías fuera de rango en {path_archivo.name}"


@pytest.mark.parametrize("path_archivo", ARCHIVOS_RECETAS)
def test_parseo_ingredientes(path_archivo):
    """Verifica el parseo de ingredientes."""
    with open(path_archivo, "r", encoding="utf-8") as f:
        texto = f.read()

    ingredientes = parsear_ingredientes(texto)
    assert isinstance(
        ingredientes, list
    ), f"Ingredientes no es lista en {path_archivo.name}"

    for ing in ingredientes:
        assert isinstance(
            ing, dict
        ), f"Ingrediente no es diccionario en {path_archivo.name}"
        assert (
            "cantidad" in ing
        ), f"Falta cantidad en ingrediente de {path_archivo.name}"
        assert "unidad" in ing, f"Falta unidad en ingrediente de {path_archivo.name}"
        assert "nombre" in ing, f"Falta nombre en ingrediente de {path_archivo.name}"
        assert ing["nombre"], f"Nombre de ingrediente vacío en {path_archivo.name}"


@pytest.mark.parametrize("path_archivo", ARCHIVOS_RECETAS)
def test_extraccion_preparacion(path_archivo):
    """Verifica la extracción de pasos de preparación."""
    with open(path_archivo, "r", encoding="utf-8") as f:
        texto = f.read()

    pasos = extraer_preparacion(texto)
    assert isinstance(pasos, list), f"Preparación no es lista en {path_archivo.name}"
    assert pasos, f"No se encontraron pasos de preparación en {path_archivo.name}"

    for paso in pasos:
        assert paso.strip(), f"Paso vacío en {path_archivo.name}"
        assert paso == paso.strip(), f"Paso con espacios extra en {path_archivo.name}"


@pytest.mark.parametrize("path_archivo", ARCHIVOS_RECETAS)
def test_normalizacion_completa(path_archivo):
    """Verifica la normalización completa de una receta."""
    with open(path_archivo, "r", encoding="utf-8") as f:
        texto = f.read()

    receta = normalizar_receta_desde_texto(texto)
    assert isinstance(
        receta, dict
    ), f"Receta normalizada no es diccionario en {path_archivo.name}"

    # Verificar estructura completa
    campos_requeridos = {
        "nombre": str,
        "url_origen": str,
        "porciones": (int, str),  # puede ser int o "Desconocido"
        "calorias_totales": (int, str),  # puede ser int o "Desconocido"
        "ingredientes": list,
        "preparacion": list,
    }

    for campo, tipo in campos_requeridos.items():
        assert campo in receta, f"Falta campo {campo} en {path_archivo.name}"
        assert isinstance(
            receta[campo], tipo
        ), f"Tipo incorrecto para {campo} en {path_archivo.name}"
