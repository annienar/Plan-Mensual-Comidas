"""
Tests para la validación de recetas.

Verifica la estructura y contenido de recetas,
independientemente del formato del archivo fuente.
"""

from pathlib import Path

import pytest

from core.config import DIR_SIN_PROCESAR
from core.extraer_txt import extraer_texto_desde_txt


def obtener_texto_receta(path_archivo: Path) -> str:
    """
    Obtiene el texto de una receta según su formato.

    Args:
        path_archivo: Ruta al archivo de receta

    Returns:
        str: Texto extraído de la receta
    """
    # Por ahora solo manejamos .txt, expandir para otros formatos
    if path_archivo.suffix.lower() == ".txt":
        return extraer_texto_desde_txt(path_archivo)
    raise ValueError(f"Formato no soportado: {path_archivo.suffix}")


# Por ahora solo procesamos .txt, expandir cuando se agreguen más formatos
ARCHIVOS_RECETAS = list(DIR_SIN_PROCESAR.glob("*.txt"))


def test_existen_archivos_recetas():
    """Asegurar que hay archivos de recetas para procesar."""
    assert (
        ARCHIVOS_RECETAS
    ), f"No se encontraron archivos de recetas en {DIR_SIN_PROCESAR}"


@pytest.mark.parametrize("path_archivo", ARCHIVOS_RECETAS)
def test_estructura_receta(path_archivo):
    """Verifica que el texto extraído tiene la estructura esperada de una receta."""
    texto = obtener_texto_receta(path_archivo)
    lines = texto.splitlines()

    # Debe tener al menos un título y contenido
    assert lines and lines[0].strip(), "La receta debe tener un título"
    assert len(lines) > 1, "La receta debe tener contenido además del título"

    # Buscar secciones principales - considerando variaciones en el idioma
    texto_lower = texto.lower()
    has_ingredients = any(
        term in texto_lower
        for term in [
            "ingredientes",
            "ingredients",
            "ingredientes:",
            "ingredients:",
            "ingredientes necesarios",
        ]
    )
    has_preparation = any(
        term in texto_lower
        for term in [
            "preparación",
            "preparacion",
            "preparation",
            "instrucciones",
            "instructions",
            "pasos",
            "método",
            "metodo",
            "elaboración",
            "elaboracion",
        ]
    )

    assert (
        has_ingredients
    ), f"No se encontró sección de ingredientes en {path_archivo.name}"
    assert (
        has_preparation
    ), f"No se encontró sección de preparación en {path_archivo.name}"


@pytest.mark.parametrize("path_archivo", ARCHIVOS_RECETAS)
def test_contenido_receta(path_archivo):
    """Verifica el contenido básico esperado en una receta."""
    texto = obtener_texto_receta(path_archivo)

    # Verificaciones básicas de contenido
    assert len(texto.splitlines()) >= 5, "La receta debe tener al menos 5 líneas"

    # Buscar elementos comunes en recetas
    texto_lower = texto.lower()

    # Verificar que hay al menos algunos números (cantidades)
    has_numbers = any(char.isdigit() for char in texto)
    assert has_numbers, f"No se encontraron cantidades numéricas en {path_archivo.name}"

    # Verificar que hay unidades de medida comunes
    unidades_medida = [
        "g",
        "kg",
        "ml",
        "l",
        "taza",
        "cucharada",
        "cdta",
        "oz",
        "lb",
        "cup",
        "tbsp",
        "tsp",
        "gramo",
        "litro",
        "pizca",
        "unidad",
        "pieza",
        "trozo",
    ]
    has_units = any(unidad in texto_lower for unidad in unidades_medida)
    assert has_units, f"No se encontraron unidades de medida en {path_archivo.name}"


@pytest.mark.parametrize("path_archivo", ARCHIVOS_RECETAS)
def test_metadatos_opcionales(path_archivo):
    """Verifica metadatos opcionales que pueden estar presentes en una receta."""
    texto = obtener_texto_receta(path_archivo)
    texto_lower = texto.lower()

    # No asertamos estos campos porque son opcionales, solo registramos su presencia
    metadatos = {
        "tiempo": any(
            term in texto_lower
            for term in [
                "tiempo",
                "time",
                "duración",
                "duracion",
                "minutos",
                "horas",
                "min",
                "hr",
            ]
        ),
        "porciones": any(
            term in texto_lower
            for term in [
                "porción",
                "porcion",
                "porciones",
                "raciones",
                "serving",
                "servings",
                "personas",
                "comensales",
            ]
        ),
        "dificultad": any(
            term in texto_lower
            for term in [
                "dificultad",
                "difficulty",
                "nivel",
                "fácil",
                "facil",
                "medio",
                "difícil",
                "dificil",
            ]
        ),
        "fuente": any(
            term in texto_lower
            for term in [
                "fuente",
                "source",
                "adapted from",
                "basado en",
                "original",
                "referencia",
                "reference",
            ]
        ),
    }

    # Registrar la presencia de metadatos para análisis posterior
    for campo, presente in metadatos.items():
        if presente:
            print(f"Info: {path_archivo.name} contiene metadatos de {campo}")
