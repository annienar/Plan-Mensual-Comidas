"""
Módulo para normalizar y extraer información estructurada de recetas.

Proporciona funciones para parsear ingredientes, pasos y metadatos.
"""

import re
from fractions import Fraction
from typing import List

# Mapa de abreviaturas a unidad estándar
_UNIDADES = {
    "g": "g",
    "gr": "g",
    "gramo": "g",
    "gramos": "g",
    "kg": "kg",
    "ml": "ml",
    "l": "l",
    "taza": "taza",
    "tazas": "taza",
    "cucharada": "cucharadas",
    "cucharadas": "cucharadas",
    "cda": "cucharadas",
    "cdas": "cucharadas",
    "cdta": "cdta",
    "tsp": "cdta",
    "cucharadita": "cdta",
    "cucharaditas": "cdta",
}

# Patrones generales
_RGX_URL = re.compile(r"https?://\S+", re.IGNORECASE)
_RGX_PORCIONES = re.compile(r"para\s*(\d+)\s*porciones?", re.IGNORECASE)
_RGX_CALORIAS = re.compile(r"calor[ií]as?:?\s*(\d+)", re.IGNORECASE)
_RGX_INGREDIENTES_HEADER = re.compile(r"^ingredientes\b", re.IGNORECASE)
_RGX_PREPARACION_HEADER = re.compile(
    r"^(pasos?|preparaci[oó]n|paso a paso)", re.IGNORECASE
)
_RGX_NOTAS_HEADER = re.compile(r"^(notas?|tips?)", re.IGNORECASE)
_RGX_FUENTE = re.compile(
    r"^(?:fuentes?|sources?|origen|adapted from|source)\s*:?\s*(.+)", re.IGNORECASE
)
_RGX_FUENTE_BRACKETS = re.compile(
    r"\[(source|origin|adapted from|found via|notes from)[^\]]*\]\s*([^\n]+)",
    re.IGNORECASE,
)


def _to_float(qty_str: str) -> float:
    """Convierte cantidad en fracción mixta, rango o número a float."""
    s = (
        qty_str.replace("½", "1/2")
        .replace("¼", "1/4")
        .replace("¾", "3/4")
        .strip()
        .lower()
    )
    raw = re.split(r"–|-|\bo\b", s)[0].strip()
    m = re.match(r"^(\d+)\s+(\d+)/(\d+)$", raw)
    if m:
        return int(m.group(1)) + int(m.group(2)) / int(m.group(3))
    if "/" in raw:
        try:
            return float(Fraction(raw))
        except Exception:
            pass
    try:
        return float(raw)
    except Exception:
        return 0.0


def parsear_linea_ingrediente(linea: str) -> dict:
    """
    Parsea una línea de texto en un ingrediente estructurado.

    Args:
        linea: Línea de texto con el ingrediente

    Returns:
        dict: Diccionario con cantidad, unidad y nombre del ingrediente
    """
    text = linea.strip()
    text = text.replace("½", "1/2").replace("¼", "1/4").replace("¾", "3/4")
    m = re.match(
        r"^(\d+\s*\d*\/?\d*|\d*\/?\d+)(?:\s*(?:–|-|o)\s*\d+)?\s*(.*)$",
        text,
        re.IGNORECASE,
    )
    if m:
        raw_qty, resto = m.groups()
        cantidad = _to_float(raw_qty)
    else:
        cantidad = 0.0
        resto = text
    resto = resto.strip()
    if resto.lower().startswith("de "):
        resto = resto[3:].strip()
    tokens = resto.split()
    unidad_tok = tokens[0].lower() if tokens else ""
    unidad = _UNIDADES.get(unidad_tok)
    if unidad:
        nombre = " ".join(tokens[1:]).strip()
    else:
        nombre = resto
        unidad = "u" if cantidad > 0 else ""
    if nombre.lower().startswith("de "):
        nombre = nombre[3:].strip()
    return {"cantidad": cantidad, "unidad": unidad, "nombre": nombre}


def parsear_ingredientes(texto: str) -> List[dict]:
    """
    Extrae y parsea todas las líneas de ingredientes de un texto.

    Args:
        texto: Texto completo de la receta

    Returns:
        List[dict]: Lista de ingredientes estructurados
    """
    lines = [line.strip() for line in texto.splitlines()]
    start = next(
        (i for i, line in enumerate(lines) if _RGX_INGREDIENTES_HEADER.match(line)),
        None,
    )
    if start is None:
        return []
    ingredientes = []
    for line in lines[start + 1 :]:
        if _RGX_PREPARACION_HEADER.match(line) or _RGX_NOTAS_HEADER.match(line):
            break
        if not line:
            continue
        clean = re.sub(r"^[-*\s]+", "", line)
        parsed = parsear_linea_ingrediente(clean)
        if parsed["nombre"]:
            ingredientes.append(parsed)
    return ingredientes


def extraer_nombre(texto: str) -> str:
    """
    Extrae el nombre de la receta (primera línea no vacía).

    Args:
        texto: Texto completo de la receta

    Returns:
        str: Nombre de la receta
    """
    for line in texto.splitlines():
        if line.strip():
            return line.strip()
    return "Desconocido"


def extraer_url_origen(texto: str) -> str:
    """
    Extrae la URL de origen de la receta.

    Args:
        texto: Texto completo de la receta

    Returns:
        str: URL de origen o 'Desconocido'
    """
    m = _RGX_URL.search(texto)
    return m.group(0) if m else "Desconocido"


def extraer_porciones(texto: str) -> int:
    """
    Extrae el número de porciones de la receta.

    Args:
        texto: Texto completo de la receta

    Returns:
        int: Número de porciones o 0 si no se encuentra
    """
    m = _RGX_PORCIONES.search(texto)
    return int(m.group(1)) if m else 0


def extraer_calorias(texto: str) -> int:
    """
    Extrae el total de calorías de la receta.

    Args:
        texto: Texto completo de la receta

    Returns:
        int: Total de calorías o 0 si no se encuentra
    """
    m = _RGX_CALORIAS.search(texto)
    return int(m.group(1)) if m else 0


def extraer_fuentes(texto: str) -> List[str]:
    """
    Extrae las fuentes de la receta.

    Args:
        texto: Texto completo de la receta

    Returns:
        List[str]: Lista de fuentes encontradas
    """
    fuentes = []

    # Buscar en cada línea
    for line in texto.splitlines():
        # Fuentes en formato normal
        m = _RGX_FUENTE.match(line.strip())
        if m:
            fuente = m.group(1).strip()
            if fuente and fuente not in fuentes:
                fuentes.append(fuente)
                continue

        # Fuentes en corchetes
        for m in _RGX_FUENTE_BRACKETS.finditer(line):
            fuente = m.group(2).strip()
            if fuente and fuente not in fuentes:
                fuentes.append(fuente)

    return fuentes


def extraer_preparacion(texto: str) -> List[str]:
    """
    Extrae la sección de preparación completa en una lista de pasos.

    Args:
        texto: Texto completo de la receta

    Returns:
        List[str]: Lista de pasos de preparación
    """
    lines = [line.strip() for line in texto.splitlines()]
    start = next(
        (i for i, line in enumerate(lines) if _RGX_PREPARACION_HEADER.match(line)), None
    )
    if start is None:
        return []
    pasos = []
    buffer = ""
    for line in lines[start + 1 :]:
        # Si encontramos notas, terminamos
        if _RGX_NOTAS_HEADER.match(line):
            break
        # Ignorar líneas vacías
        if not line:
            continue
        m = re.match(r"^(\d+)\.?\s*(.*)", line)
        if m:
            if buffer:
                pasos.append(buffer.strip())
            buffer = m.group(2).strip()
        else:
            buffer += " " + line
    if buffer:
        pasos.append(buffer.strip())
    return pasos


def normalizar_receta_desde_texto(texto: str) -> dict:
    """
    Normaliza un texto de receta en un diccionario estructurado.

    Args:
        texto: Texto completo de la receta

    Returns:
        dict: Receta normalizada con todos sus campos
    """
    return {
        "nombre": extraer_nombre(texto),
        "url_origen": extraer_url_origen(texto),
        "porciones": extraer_porciones(texto),
        "calorias_totales": extraer_calorias(texto),
        "ingredientes": parsear_ingredientes(texto),
        "preparacion": extraer_preparacion(texto),
        "fuentes": extraer_fuentes(texto),
    }
