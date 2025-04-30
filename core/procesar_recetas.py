# core/procesar_recetas.py

import os
import shutil
import json
from core.logger import configurar_logger, log_info, log_warning, log_error
from core.notificaciones import (
    log_creacion_carpeta,
    log_movimiento_archivo,
    log_creacion_archivo,
    log_receta_normalizada,
    log_error_archivo,
)
from core.normalizador_recetas import normalizar_receta_desde_texto
from core.extraer_txt import extraer_texto_desde_txt
from core.extraer_pdf import extraer_texto_desde_pdf
from core.extraer_ocr import extraer_texto_desde_ocr

logger = configurar_logger("procesar_recetas")


def procesar_archivo(path_archivo) -> bool:
    """
    Procesa un único archivo de receta:
      1. Extrae texto según la extensión
      2. Normaliza el contenido
      3. Crea carpetas de salida
      4. Copia el original a Receta Original
      5. Guarda JSON en Recetas JSON
      6. Elimina el archivo original
    """
    ext = os.path.splitext(path_archivo)[1].lower().lstrip('.')
    log_info(f"📄 Procesando: {path_archivo}")

    base = os.path.splitext(os.path.basename(path_archivo))[0]
    destino_original = f"recetas/procesadas/Receta Original/{os.path.basename(path_archivo)}"
    ruta_json = f"recetas/procesadas/Recetas JSON/{base}.json"

    try:
        # 1. EXTRAER TEXTO
        if ext == "txt":
            texto = extraer_texto_desde_txt(path_archivo)
        elif ext == "pdf":
            texto = extraer_texto_desde_pdf(path_archivo)
            if not texto.strip():
                log_warning("⚠️ PDF sin texto; aplicando OCR…")
                texto = extraer_texto_desde_ocr(path_archivo)
        elif ext in ("jpg", "jpeg", "png"):
            texto = extraer_texto_desde_ocr(path_archivo)
        else:
            log_warning(f"⚠️ Tipo de archivo no soportado: {path_archivo}")
            return False

        # 2. NORMALIZAR
        receta = normalizar_receta_desde_texto(texto)
        log_receta_normalizada(receta.get("nombre", "Sin nombre"))

        # 3. CREAR CARPETAS DE SALIDA
        for carpeta in (os.path.dirname(destino_original), os.path.dirname(ruta_json)):
            if not os.path.exists(carpeta):
                os.makedirs(carpeta, exist_ok=True)
                log_creacion_carpeta(carpeta)

        # 4. COPIAR ORIGINAL
        shutil.copy2(path_archivo, destino_original)
        log_movimiento_archivo(path_archivo, destino_original)

        # 5. GUARDAR JSON
        with open(ruta_json, "w", encoding="utf-8") as f:
            json.dump(receta, f, ensure_ascii=False, indent=2)
        log_creacion_archivo(ruta_json)

        # 6. ELIMINAR ORIGINAL
        os.remove(path_archivo)
        log_info("✅ Procesado correctamente.")
        return True

    except Exception as e:
        log_error_archivo(path_archivo, f"Error general: {e}")
        # Limpieza de copia parcial
        if os.path.exists(destino_original):
            try:
                os.remove(destino_original)
                log_warning(f"⚠️ Limpieza: se eliminó la copia de {destino_original}")
            except OSError:
                pass
        return False


def procesar_todo_en_sin_procesar():
    """
    Procesa todos los archivos en recetas/sin_procesar/ y muestra un resumen.
    """
    carpeta = "recetas/sin_procesar"
    archivos = [f for f in os.listdir(carpeta)
                if f.lower().endswith((".txt", ".pdf", ".jpg", ".jpeg", ".png"))]

    if not archivos:
        log_info("📂 No hay archivos para procesar en recetas/sin_procesar.")
        return

    total = len(archivos)
    exitosos = 0
    for nombre in archivos:
        if procesar_archivo(os.path.join(carpeta, nombre)):
            exitosos += 1

    log_info(f"🏁 Resumen: {exitosos}/{total} archivos procesados con éxito.")


if __name__ == "__main__":
    procesar_todo_en_sin_procesar()