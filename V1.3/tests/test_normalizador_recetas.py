from core.logger import configurar_logger
logger = configurar_logger("test_normalizador_recetas")

import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.normalizador_recetas import normalizar_receta_desde_texto

def probar_normalizador_con_archivo(ruta_txt):
    if not os.path.exists(ruta_txt):
        logger.info(f"Archivo no encontrado: {ruta_txt}")
        return

    with open(ruta_txt, "r", encoding="utf-8") as f:
        texto = f.read()

    receta = normalizar_receta_desde_texto(texto)

    logger.info("\n=== Receta normalizada ===")
    logger.info(json.dumps(receta, indent=2, ensure_ascii=False))

    ruta_salida = ruta_txt.replace(".txt", "_normalizada.json")
    with open(ruta_salida, "w", encoding="utf-8") as f:
        json.dump(receta, f, ensure_ascii=False, indent=2)
    logger.info(f"\n✅ Resultado guardado en: {ruta_salida}")

if __name__ == "__main__":
    probar_normalizador_con_archivo("recetas/pasta_ajo_albahaca.txt")
