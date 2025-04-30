from core.logger import configurar_logger
logger = configurar_logger("test_procesar_recetas")

import os
import shutil
import json
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.normalizador_recetas import normalizar_receta_desde_texto

ruta_sin_procesar = "recetas/sin_procesar"
ruta_procesadas = "recetas/procesadas"

def procesar_lote():
    if not os.path.exists(ruta_sin_procesar):
        logger.info(f"No existe la carpeta: {ruta_sin_procesar}")
        return

    for archivo in os.listdir(ruta_sin_procesar):
        if archivo.endswith(".txt"):
            ruta_txt = os.path.join(ruta_sin_procesar, archivo)
            logger.info(f"📄 Procesando {archivo}...")

            with open(ruta_txt, "r", encoding="utf-8") as f:
                texto = f.read()

            receta = normalizar_receta_desde_texto(texto)

            base_nombre = os.path.splitext(archivo)[0]
            ruta_json = os.path.join(ruta_procesadas, base_nombre + ".json")

            with open(ruta_json, "w", encoding="utf-8") as f:
                json.dump(receta, f, ensure_ascii=False, indent=2)

            shutil.move(ruta_txt, os.path.join(ruta_procesadas, archivo))
            logger.info(f"✅ Guardado como {ruta_json} y movido a procesadas.")

if __name__ == "__main__":
    procesar_lote()
