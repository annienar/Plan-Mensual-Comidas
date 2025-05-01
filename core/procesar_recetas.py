# core/procesar_recetas.py

"""
Módulo principal para el procesamiento de recetas.

Maneja la extracción, normalización y almacenamiento de recetas.
"""

import json
from pathlib import Path
from typing import List

from core.config import (
    DIR_RECETAS_JSON,
    DIR_RECETAS_ORIGINALES,
    DIR_SIN_PROCESAR,
    ENCODING_DEFAULT,
    es_extension_soportada,
    obtener_tipo_archivo,
)
from core.extraer_ocr import extraer_texto_desde_imagen
from core.extraer_pdf import extraer_texto_desde_pdf
from core.extraer_txt import extraer_texto_desde_txt
from core.logger import configurar_logger, log_info, log_warning
from core.normalizador_recetas import normalizar_receta_desde_texto
from core.notificaciones import (
    log_carpeta_vacia,
    log_codificacion_invalida,
    log_creacion_archivo,
    log_error_archivo,
    log_error_parseo,
    log_formato_invalido,
    log_fuentes_encontradas,
    log_metadatos_incompletos,
    log_movimiento_archivo,
    log_receta_normalizada,
)

logger = configurar_logger("procesar_recetas")


def validar_metadatos(receta: dict) -> List[str]:
    """
    Valida que la receta tenga todos los metadatos requeridos.

    Args:
        receta: Diccionario con los datos de la receta

    Returns:
        List[str]: Lista de campos faltantes
    """
    campos_requeridos = ["nombre", "ingredientes", "preparacion"]
    faltantes = []

    for campo in campos_requeridos:
        if not receta.get(campo):
            faltantes.append(campo)

    # Validaciones específicas
    if not isinstance(receta.get("porciones"), int) or receta["porciones"] <= 0:
        faltantes.append("porciones")

    return faltantes


def procesar_archivo(path_archivo: Path) -> bool:
    """
    Procesa un único archivo de receta.

    Args:
        path_archivo: Ruta al archivo a procesar

    Returns:
        bool: True si el procesamiento fue exitoso, False en caso contrario
    """
    if not es_extension_soportada(path_archivo):
        log_formato_invalido(
            str(path_archivo), f"Extensión no soportada: {path_archivo.suffix}"
        )
        return False

    log_info(f"📄 Procesando: {path_archivo}")

    destino_original = DIR_RECETAS_ORIGINALES / path_archivo.name
    ruta_json = DIR_RECETAS_JSON / f"{path_archivo.stem}.json"

    try:
        # 1. EXTRAER TEXTO
        tipo_archivo = obtener_tipo_archivo(path_archivo)
        try:
            if tipo_archivo == "texto":
                texto = extraer_texto_desde_txt(path_archivo)
            elif tipo_archivo == "pdf":
                texto = extraer_texto_desde_pdf(path_archivo)
                if not texto.strip():
                    log_warning("⚠️ PDF sin texto; aplicando OCR…")
                    texto = extraer_texto_desde_imagen(path_archivo)
            elif tipo_archivo == "imagen":
                texto = extraer_texto_desde_imagen(path_archivo)
            else:
                log_formato_invalido(
                    str(path_archivo), f"Tipo de archivo no soportado: {tipo_archivo}"
                )
                return False
        except UnicodeError:
            log_codificacion_invalida(str(path_archivo))
            return False

        # 2. NORMALIZAR Y VALIDAR
        try:
            receta = normalizar_receta_desde_texto(texto)

            # Validar fuentes si existen
            if "fuentes" in receta and receta["fuentes"]:
                log_fuentes_encontradas(receta["nombre"], len(receta["fuentes"]))

            # Validar metadatos
            faltantes = validar_metadatos(receta)
            if faltantes:
                log_metadatos_incompletos(receta["nombre"], faltantes)

            log_receta_normalizada(receta["nombre"])

        except Exception as e:
            log_error_parseo(path_archivo.name, "normalización", str(e))
            return False

        # 3. CREAR CARPETAS DE SALIDA
        destino_original.parent.mkdir(parents=True, exist_ok=True)
        ruta_json.parent.mkdir(parents=True, exist_ok=True)

        # 4. COPIAR ORIGINAL
        destino_original.write_bytes(path_archivo.read_bytes())
        log_movimiento_archivo(str(path_archivo), str(destino_original))

        # 5. GUARDAR JSON
        ruta_json.write_text(
            json.dumps(receta, ensure_ascii=False, indent=2), encoding=ENCODING_DEFAULT
        )
        log_creacion_archivo(str(ruta_json))

        # 6. ELIMINAR ORIGINAL
        path_archivo.unlink()
        log_info("✅ Procesado correctamente.")
        return True

    except Exception as e:
        log_error_archivo(str(path_archivo), f"Error general: {e}")
        # Limpieza de copia parcial
        if destino_original.exists():
            try:
                destino_original.unlink()
                log_warning(f"⚠️ Limpieza: se eliminó la copia de {destino_original}")
            except OSError:
                pass
        return False


def procesar_todo_en_sin_procesar() -> bool:
    """
    Procesa todos los archivos pendientes en el directorio sin_procesar.

    Returns:
        bool: True si todos los archivos se procesaron correctamente
    """
    archivos = [
        f
        for f in DIR_SIN_PROCESAR.iterdir()
        if f.is_file() and es_extension_soportada(f)
    ]

    if not archivos:
        log_carpeta_vacia(str(DIR_SIN_PROCESAR))
        return True

    exitos = 0
    for archivo in archivos:
        if procesar_archivo(archivo):
            exitos += 1

    return exitos == len(archivos)


if __name__ == "__main__":
    procesar_todo_en_sin_procesar()
