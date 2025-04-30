# tests/test_parser_unit.py
from pathlib import Path
import pytest

from core.normalizador_recetas import parsear_linea_ingrediente, parsear_ingredientes

# --- Setup común: inyectar receta compleja antes de glob ---
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

# Configurar entorno: fixture que se ejecuta antes de cada módulo
def pytest_fixture_setup_receta_compleja(request):
    _setup_receta_compleja()

# 2) Test dinámico de parsear_ingredientes para todos los .txt incluyendo la compleja de parsear_ingredientes para todos los .txt incluyendo la compleja
CARPETA_SIN_PROCESAR = Path(__file__).resolve().parents[1] / "recetas" / "sin_procesar"
TXT_FILES = list(CARPETA_SIN_PROCESAR.glob("*.txt"))
if not TXT_FILES:
    pytest.skip(f"No hay archivos .txt en {CARPETA_SIN_PROCESAR}", allow_module_level=True)

@pytest.mark.parametrize("path_archivo", TXT_FILES)
def test_parsear_ingredientes_completo(path_archivo):
    """
    Para cada .txt en recetas/sin_procesar/, verifica que parsear_ingredientes
    extrae al menos un ingrediente válido.
    """
    texto = Path(path_archivo).read_text(encoding="utf-8")
    ingredientes = parsear_ingredientes(texto)
    assert isinstance(ingredientes, list), "La función debe devolver una lista"
    assert ingredientes, f"No se extrajo ningún ingrediente de {path_archivo.name}"

