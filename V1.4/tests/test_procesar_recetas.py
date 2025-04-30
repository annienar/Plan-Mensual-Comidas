# tests/test_procesar_recetas.py
"""
Test end-to-end para procesar todas las recetas en recetas/sin_procesar/.
Verifica que:
  • Se crean las carpetas procesadas/Receta Original y Recetas JSON.
  • Cada archivo fuente se copia a Receta Original.
  • Cada receta genera un archivo JSON en Recetas JSON con estructura válida.
"""
import os
import shutil
import json
import pytest
from core.procesar_recetas import procesar_todo_en_sin_procesar

# Rutas del proyecto
BASE_DIR     = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SIN_PROCESAR = os.path.join(BASE_DIR, 'recetas', 'sin_procesar')
PROCESADAS   = os.path.join(BASE_DIR, 'recetas', 'procesadas')
ORIGINAL     = os.path.join(PROCESADAS, 'Receta Original')
JSON_DIR     = os.path.join(PROCESADAS, 'Recetas JSON')

@pytest.fixture(autouse=True)
def entorno_limpio():
    # 1) Respaldar los originales
    backup_sin = SIN_PROCESAR + "_backup"
    if os.path.exists(backup_sin):
        shutil.rmtree(backup_sin)
    shutil.copytree(SIN_PROCESAR, backup_sin)

    # 2) Limpiar carpeta procesadas
    if os.path.exists(PROCESADAS):
        shutil.rmtree(PROCESADAS)

    yield

    # 3) Restaurar los originales
    if os.path.exists(SIN_PROCESAR):
        shutil.rmtree(SIN_PROCESAR)
    shutil.copytree(backup_sin, SIN_PROCESAR)
    shutil.rmtree(backup_sin)

    # 4) Limpiar procesadas por si queda algo
    if os.path.exists(PROCESADAS):
        shutil.rmtree(PROCESADAS)


def test_procesar_todo_en_sin_procesar():
    archivos = os.listdir(SIN_PROCESAR)
    if not archivos:
        pytest.skip("No hay archivos en recetas/sin_procesar para procesar")

    # Ejecutar el procesamiento completo
    procesar_todo_en_sin_procesar()

    # Verificar creación de carpetas
    assert os.path.isdir(ORIGINAL), "No se creó la carpeta 'Receta Original'"
    assert os.path.isdir(JSON_DIR), "No se creó la carpeta 'Recetas JSON'"

    # Para cada archivo de entrada, comprobar copia y JSON
    for nombre in archivos:
        ruta_original = os.path.join(ORIGINAL, nombre)
        assert os.path.exists(ruta_original), f"El archivo {nombre} no fue copiado a 'Receta Original'"

        nombre_json = os.path.splitext(nombre)[0] + '.json'
        ruta_json = os.path.join(JSON_DIR, nombre_json)
        assert os.path.exists(ruta_json), f"No se creó JSON para {nombre}"

        # Validar contenido mínimo del JSON
        with open(ruta_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert 'nombre' in data, f"JSON {nombre_json} sin campo 'nombre'"
        assert isinstance(data.get('ingredientes'), list), f"JSON {nombre_json} 'ingredientes' no es lista"
        assert data['ingredientes'], f"JSON {nombre_json} tiene lista de ingredientes vacía"
