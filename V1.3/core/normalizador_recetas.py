from core.logger import configurar_logger
logger = configurar_logger("normalizador_recetas")

import re
import json
import logging
import os
from datetime import datetime

# Crear carpeta de logs si no existe
os.makedirs(".log", exist_ok=True)

# Crear log con timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_path = f".log/normalizador_{timestamp}.log"
logging.basicConfig(
    filename=log_path,
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
# sustituido por configurar_logger

def normalizar_receta_desde_texto(texto):
    logger.info("Iniciando normalización de receta")
    nombre = extraer_nombre(texto)
    calorias = extraer_calorias(texto)
    ingredientes = parsear_ingredientes(texto)
    preparacion = extraer_preparacion(texto)
    tags = inferir_tags(ingredientes, preparacion)

    receta = {
        "nombre": nombre,
        "calorias": calorias,
        "ingredientes": ingredientes,
        "preparacion": preparacion,
        "tags": tags
    }

    logger.info("Receta normalizada correctamente")
    logger.info(json.dumps(receta, indent=2, ensure_ascii=False))
    return receta

def extraer_nombre(texto):
    lineas = texto.strip().splitlines()
    for linea in lineas:
        if linea.strip():
            return linea.strip()
    return "Receta sin nombre"

def extraer_calorias(texto):
    match = re.search(r"(?:[Cc]alor[ií]as|[Cc]alories)[:\s]+(\d+)", texto)
    return int(match.group(1)) if match else 0

def parsear_ingredientes(texto):
    patrones = ["ingredientes", "ingredients"]
    ingredientes = []
    for encabezado in patrones:
        match = re.search(rf"{encabezado}[:\n]", texto, re.IGNORECASE)
        if match:
            seccion = texto[match.end():]
            lineas = seccion.strip().splitlines()
            for linea in lineas:
                if not linea.strip() or any(p in linea.lower() for p in ["preparación", "instrucciones", "preparation", "instructions"]):
                    break
                ingrediente = parsear_linea_ingrediente(linea)
                if ingrediente:
                    ingredientes.append(ingrediente)
            break
    return ingredientes

def parsear_linea_ingrediente(linea):
    patron = r"(?P<cantidad>\d+(\.\d+)?)(\s+)?(?P<unidad>\w+)?\s+(?P<nombre>.+)"
    match = re.search(patron, linea.strip())
    if match:
        nombre = match.group("nombre").strip()
        if nombre.lower().startswith("de "):
            nombre = nombre[3:].strip()
        elif nombre.lower().startswith("of "):
            nombre = nombre[3:].strip()
        return {
            "nombre": nombre,
            "cantidad": float(match.group("cantidad")),
            "unidad": match.group("unidad") or "unidad"
        }
    return None

def extraer_preparacion(texto):
    posibles = ["preparación", "instrucciones", "preparation", "instructions"]
    for encabezado in posibles:
        match = re.search(rf"{encabezado}[:\n]", texto, re.IGNORECASE)
        if match:
            return texto[match.end():].strip()
    return ""

def inferir_tags(ingredientes, preparacion):
    tags = []
    if any("huevo" in i["nombre"].lower() or "egg" in i["nombre"].lower() for i in ingredientes):
        tags.append("proteico")
    if len(ingredientes) <= 4:
        tags.append("simple")
    return tags
