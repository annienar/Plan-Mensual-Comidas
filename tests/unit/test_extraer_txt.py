# tests/test_extraer_txt.py
"""
Tests para la extracción de texto de archivos .txt.

Verifica la correcta extracción de texto plano desde archivos .txt,
incluyendo manejo de codificación y preservación del contenido.
"""

from pathlib import Path

import pytest

from core.config import DIR_SIN_PROCESAR
from core.extraer_txt import extraer_texto_desde_txt

# Obtener todos los archivos .txt
ARCHIVOS_TXT = list(DIR_SIN_PROCESAR.glob("*.txt"))


def test_existen_archivos_txt():
    """Asegurar que hay archivos .txt para procesar."""
    assert ARCHIVOS_TXT, f"No se encontraron archivos .txt en {DIR_SIN_PROCESAR}"


@pytest.mark.parametrize("path_archivo", ARCHIVOS_TXT)
def test_extraer_texto_desde_txt(path_archivo):
    """Verifica la extracción básica de texto."""
    texto = extraer_texto_desde_txt(path_archivo)

    # Verificar que devuelve un string no vacío
    assert isinstance(
        texto, str
    ), f"Extractor no devolvió string en {path_archivo.name}"
    assert texto.strip(), f"Extractor devolvió texto vacío para {path_archivo.name}"

    # Verificar que el contenido coincide exactamente con el archivo
    with open(path_archivo, "r", encoding="utf-8") as f:
        contenido_original = f.read()
    assert (
        texto == contenido_original
    ), f"El contenido extraído no coincide con el original en {path_archivo.name}"


@pytest.mark.parametrize("path_archivo", ARCHIVOS_TXT)
def test_manejo_codificacion(path_archivo):
    """Verifica el correcto manejo de caracteres especiales y codificación."""
    texto = extraer_texto_desde_txt(path_archivo)

    # Verificar que no hay caracteres de codificación incorrecta
    caracteres_problematicos = ["", "□", ""]
    for char in caracteres_problematicos:
        assert (
            char not in texto
        ), f"Encontrado carácter de codificación incorrecta '{char}' en {path_archivo.name}"

    # Verificar que los caracteres especiales comunes se preservan
    caracteres_especiales = ["á", "é", "í", "ó", "ú", "ñ", "ü"]
    for char in caracteres_especiales:
        if char in texto:
            assert (
                char in texto
            ), f"El carácter especial '{char}' no se preservó en {path_archivo.name}"


@pytest.mark.parametrize("path_archivo", ARCHIVOS_TXT)
def test_estructura_archivo_txt(path_archivo):
    """Verifica la estructura básica del archivo de texto."""
    texto = extraer_texto_desde_txt(path_archivo)
    lines = texto.splitlines()

    # Verificaciones básicas de estructura del archivo
    assert lines, f"No se encontraron líneas en {path_archivo.name}"
    assert len(lines) > 1, f"El archivo {path_archivo.name} solo tiene una línea"

    # Verificar formato del texto
    assert (
        texto == texto.strip()
    ), f"El texto contiene espacios en blanco innecesarios al inicio o final en {path_archivo.name}"

    # Verificar que no hay líneas vacías consecutivas
    for i in range(len(lines) - 1):
        assert not (
            lines[i].strip() == "" and lines[i + 1].strip() == ""
        ), f"Encontradas líneas vacías consecutivas en {path_archivo.name}"

    # Verificar longitud máxima de línea (readability)
    max_line_length = 120
    long_lines = [i + 1 for i, line in enumerate(lines) if len(line) > max_line_length]
    assert (
        not long_lines
    ), f"Líneas demasiado largas (>{max_line_length} caracteres) en líneas {long_lines} de {path_archivo.name}"

    # Verificar que no hay caracteres de control excepto saltos de línea
    control_chars = [
        char for char in texto if char.isprintable() is False and char != "\n"
    ]
    assert (
        not control_chars
    ), f"Encontrados caracteres de control no permitidos en {path_archivo.name}: {control_chars}"
