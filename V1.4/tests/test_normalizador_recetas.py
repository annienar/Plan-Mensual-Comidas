# tests/test_normalizador_recetas.py
import os
import glob
import pytest

from core.extraer_txt   import extraer_texto_desde_txt
from core.extraer_pdf   import extraer_texto_desde_pdf
from core.extraer_ocr   import extraer_texto_desde_ocr
from core.normalizador_recetas import normalizar_receta_desde_texto

# Ruta absoluta a la carpeta de recetas reales
RECIPE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "recetas", "sin_procesar")
)

# Recopilar todos los archivos de receta
ALL_FILES = glob.glob(os.path.join(RECIPE_DIR, "*"))

@pytest.mark.parametrize("path_archivo", ALL_FILES)
def test_normalizador_recetas(path_archivo):
    """
    Para cada receta (txt, pdf, jpg, png) extrae el texto con el módulo correspondiente,
    luego lo normaliza y chequea que tenga nombre, lista de ingredientes y metadatos mínimos.
    """
    ext = os.path.splitext(path_archivo)[1].lower()

    # Extraer texto según el tipo de archivo
    if ext == ".txt":
        texto = extraer_texto_desde_txt(path_archivo)
    elif ext == ".pdf":
        texto = extraer_texto_desde_pdf(path_archivo)
    elif ext in (".jpg", ".jpeg", ".png"):
        texto = extraer_texto_desde_ocr(path_archivo)
    else:
        pytest.skip(f"Formato no soportado en este test: {ext}")

    # Normalizar la receta
    receta = normalizar_receta_desde_texto(texto)

    # Validaciones básicas
    assert isinstance(receta, dict),    f"Salida no es dict para {path_archivo}"
    assert receta.get("nombre"),        f"Falta nombre en {path_archivo}"
    assert isinstance(receta.get("ingredientes"), list), f"Ingredientes no listado en {path_archivo}"
    assert receta["ingredientes"],     f"No se detectaron ingredientes en {path_archivo}"
    assert "url_origen" in receta,     f"Falta campo url_origen en {path_archivo}"
    assert "porciones" in receta,      f"Falta campo porciones en {path_archivo}"
    assert isinstance(receta["porciones"], int), f"Porciones debe ser int en {path_archivo}"
