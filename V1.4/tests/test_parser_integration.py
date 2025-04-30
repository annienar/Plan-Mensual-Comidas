# tests/test_parser_integration.py
import os
import pytest
from pathlib import Path

from core.extraer_txt import extraer_texto_desde_txt
from core.normalizador_recetas import normalizar_receta_desde_texto
from core.procesar_recetas import procesar_todo_en_sin_procesar
from core.generar_md import generar_md_todas

# Directorio base de recetas sin procesar
CARPETA_SIN_PROCESAR = Path(__file__).resolve().parents[1] / 'recetas' / 'sin_procesar'
TXT_FILES = list(CARPETA_SIN_PROCESAR.glob('*.txt'))
if not TXT_FILES:
    pytest.skip(f"No hay archivos .txt en {CARPETA_SIN_PROCESAR}", allow_module_level=True)

@pytest.mark.parametrize('path_archivo', TXT_FILES)
def test_integracion_txt_parser(path_archivo):
    # 1) Extraer texto
    texto = extraer_texto_desde_txt(str(path_archivo))
    assert texto, "El extractor TXT devolvió texto vacío"

    # 2) Normalizar
    receta = normalizar_receta_desde_texto(texto)

    # 3) Estructura mínima
    assert isinstance(receta, dict)
    for campo in ('nombre', 'url_origen', 'porciones', 'ingredientes', 'preparacion'):
        assert campo in receta, f"Falta campo '{campo}' en la receta"

    # 4) Validaciones
    assert receta['nombre'], "El nombre no debe estar vacío"
    assert isinstance(receta['porciones'], int), "Porciones debe ser int"
    assert isinstance(receta['ingredientes'], list) and receta['ingredientes'], "Debe haber al menos un ingrediente"
    assert isinstance(receta['preparacion'], list), "Preparación debe ser lista"


def test_generacion_md_para_receta_compleja():
    """
    Procesa todos los .txt (incluida la receta compleja) y genera MD;
    comprueba contenido clave en el MD de la receta compleja.
    """
    # Preparar la receta compleja en sin_procesar
    contenido_complejo = '''Receta Compleja Gourmet
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
    sin_pro = CARPETA_SIN_PROCESAR
    path_complejo = sin_pro / 'receta_compleja_para_test.txt'
    # Escribir el archivo de prueba
    path_complejo.write_text(contenido_complejo, encoding='utf-8')

    # 1) Procesar y generar JSON y MD
    procesar_todo_en_sin_procesar()
    generar_md_todas()

    # 2) Ubicar el MD generado
    base_dir = Path(__file__).resolve().parents[1]
    md_file = base_dir / 'recetas' / 'procesadas' / 'Recetas MD' / 'receta_compleja_para_test.md'
    assert md_file.exists(), f"No se generó el MD para la receta compleja: {md_file}"

    content = md_file.read_text(encoding='utf-8')
    # Verificaciones específicas
    assert '# Receta Compleja Gourmet' in content
    assert '- 1 1/2 taza de harina de trigo integral' in content
    assert '- 100 g de chocolate troceado' in content
    assert '- sal al gusto' in content

