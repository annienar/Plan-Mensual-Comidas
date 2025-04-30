import sys
import os
import json
from pathlib import Path
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.normalizador_recetas import normalizar_receta_desde_texto
from core.logger import configurar_logger

logger = configurar_logger("test_gestor")

def procesar_desde_recetas_simulado():
    load_dotenv()
    env_vars = ["NOTION_TOKEN", "NOTION_RECETAS_DB", "NOTION_ALACENA_DB", "NOTION_INGREDIENTES_DB", "NOTION_LISTA_COMPRAS_DB"]
    for var in env_vars:
        if not os.environ.get(var):
            print("⚠️ Falta variable en .env:", var)
            logger.warning(f"Falta variable en .env: {var}")
            return

    ruta = "recetas/sin_procesar"
    destino_original = "recetas/procesadas/Receta Original"
    destino_json = "recetas/procesadas/Recetas JSON"

    os.makedirs(destino_original, exist_ok=True)
    os.makedirs(destino_json, exist_ok=True)

    archivos = [f for f in os.listdir(ruta) if f.endswith(".txt")]
    if not archivos:
        print("No hay recetas para procesar.")
        logger.info("No hay recetas para procesar.")
        return

    archivo = archivos[0]
    ruta_txt = os.path.join(ruta, archivo)
    print("📄 Procesando archivo:", archivo)
    logger.info(f"Procesando archivo: {archivo}")

    with open(ruta_txt, "r", encoding="utf-8") as f:
        texto = f.read()

    receta = normalizar_receta_desde_texto(texto)

    base_nombre = os.path.splitext(archivo)[0]
    ruta_json = os.path.join(destino_json, base_nombre + ".json")
    with open(ruta_json, "w", encoding="utf-8") as f:
        json.dump(receta, f, ensure_ascii=False, indent=2)

    os.rename(ruta_txt, os.path.join(destino_original, archivo))
    print("✅ Simulación completa. JSON guardado en:", ruta_json)
    logger.info(f"Simulación completa. JSON guardado en: {ruta_json}")

if __name__ == "__main__":
    procesar_desde_recetas_simulado()
