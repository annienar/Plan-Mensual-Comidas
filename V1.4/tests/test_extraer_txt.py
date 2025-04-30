# tests/test_extraer_txt.py
import sys
from pathlib import Path
import pytest

from core.extraer_txt import extraer_texto_desde_txt

# Setup: inyecta una receta compleja si no hay .txt
def _setup_receta_compleja():
    contenido = '''Receta Compleja Gourmet
https://www.ejemplo.com/recetas/receta-compleja-gourmet

Ingredientes para 2–4 porciones
1 1/2 taza de harina de trigo integral
¾ taza de avena (puedes usar copos grandes)
0.25 kg mantequilla sin sal
½ cdta pimienta negra recién molida
2–3 tomates medianos, cortados en cubos
Sal al gusto

Sección mixta de cantidades:
- 1 huevo
- 1 o 2 cucharadas de aceite de oliva virgen extra
- ⅓ taza de azúcar moreno
- 0.5 l leche (puede ser vegetal)

Ingredientes en tabla simulada:
Cantidad   Unidad     Ingrediente
100g       chocolate  troceado
2          ramitas    tomillo fresco

Preparación:
1. Precalentar el horno a 180 °C.
2. En un bol grande, mezclar harina, avena y azúcar.
3. Añadir mantequilla y trabajar hasta migas finas.
4. Incorporar huevo y leche, batiendo hasta homogeneizar.
5. Agregar tomates, tomillo y especias; ajustar sal.
6. Verter en molde engrasado.
7. Hornear 25–30 minutos o hasta dorar.

Notas:
- Para versión vegana, sustituir huevo por 1 cda de linaza molida + 3 cda agua.
- Esta receta admite variaciones: queso rallado, nueces, hierbas secas.
'''  # noqa
    root = Path(__file__).resolve().parents[1]
    sin_pro = root / 'recetas' / 'sin_procesar'
    sin_pro.mkdir(parents=True, exist_ok=True)
    path = sin_pro / 'receta_compleja_para_test.txt'
    path.write_text(contenido, encoding='utf-8')

# Ejecutar setup
_setup_receta_compleja()

# Carpeta de entrada con archivos TXT
CARPETA_SIN_PROCESAR = Path(__file__).resolve().parents[1] / "recetas" / "sin_procesar"
TXT_FILES = [p for p in CARPETA_SIN_PROCESAR.iterdir() if p.suffix.lower() == ".txt"]

def test_existen_archivos_txt_para_normalizar():
    """Asegurar que hay al menos un .txt para normalizar."""
    assert TXT_FILES, f"No se encontraron archivos .txt en {CARPETA_SIN_PROCESAR}"

@pytest.mark.parametrize("path_archivo", TXT_FILES)
def test_extraer_texto_desde_txt(path_archivo):
    """Verifica que extraer_texto_desde_txt devuelve contenido no vacío para cada .txt."""
    texto = extraer_texto_desde_txt(str(path_archivo))
    assert isinstance(texto, str), f"Extractor no devolvió string en {path_archivo.name}"
    assert texto.strip(), f"Extractor devolvió texto vacío para {path_archivo.name}"

