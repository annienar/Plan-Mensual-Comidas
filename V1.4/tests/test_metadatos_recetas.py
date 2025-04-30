import re
from fractions import Fraction

# Mapa de abreviaturas a unidad estándar
_UNIDADES = {
    'g': 'g', 'gr': 'g', 'gramo': 'g', 'gramos': 'g',
    'kg': 'kg',
    'ml': 'ml', 'l': 'l',
    'taza': 'taza', 'tazas': 'taza',
    'cucharada': 'cucharadas', 'cucharadas': 'cucharadas', 'cda': 'cucharadas', 'cdas': 'cucharadas',
    'cdta': 'cdta', 'tsp': 'cdta', 'cucharadita': 'cdta', 'cucharaditas': 'cdta',
}

# Patrones generales
_RGX_URL = re.compile(r'https?://\S+', re.IGNORECASE)
_RGX_PORCIONES = re.compile(r'para\s*(\d+)\s*porciones?', re.IGNORECASE)
_RGX_CALORIAS = re.compile(r'calor[ií]as?:?\s*(\d+)', re.IGNORECASE)
_RGX_INGREDIENTES_HEADER = re.compile(r'^ingredientes\b', re.IGNORECASE)
_RGX_PREPARACION_HEADER = re.compile(r'^(pasos?|preparaci[oó]n|paso a paso)', re.IGNORECASE)
_RGX_NOTAS_HEADER = re.compile(r'^(notas?|tips?)', re.IGNORECASE)


def _to_float(qty_str: str) -> float:
    """Convierte cantidad en fracción mixta, rango o número a float."""
    s = qty_str.replace('½', '1/2').replace('¼', '1/4').replace('¾', '3/4').strip().lower()
    raw = re.split(r'–|-|\bo\b', s)[0].strip()
    # Mixed fraction
    m = re.match(r'^(\d+)\s+(\d+)/(\d+)$', raw)
    if m:
        return int(m.group(1)) + int(m.group(2)) / int(m.group(3))
    # Simple fraction
    if '/' in raw:
        try:
            return float(Fraction(raw))
        except Exception:
            pass
    # Plain number
    try:
        return float(raw)
    except Exception:
        return 0.0


def parsear_linea_ingrediente(linea: str) -> dict:
    """Parsea una línea de ingrediente en cantidad, unidad y nombre."""
    text = linea.strip()
    # Normalizar fracciones Unicode
    text = text.replace('½', '1/2').replace('¼', '1/4').replace('¾', '3/4')
    # Captura cantidad (incluye rangos) y resto
    m = re.match(
        r'^(\d+\s*\d*\/?\d*|\d*\/?\d+)(?:\s*(?:–|-|o)\s*\d+)?\s*(.*)$',
        text,
        re.IGNORECASE
    )
    if m:
        raw_qty, resto = m.groups()
        cantidad = _to_float(raw_qty)
    else:
        cantidad = 0.0
        resto = text
    resto = resto.strip()
    # Eliminar prefijo 'de '
    if resto.lower().startswith('de '):
        resto = resto[3:].strip()
    tokens = resto.split()
    unidad_tok = tokens[0].lower() if tokens else ''
    unidad = _UNIDADES.get(unidad_tok)
    if unidad:
        nombre = ' '.join(tokens[1:]).strip()
    else:
        nombre = resto
        unidad = 'u' if cantidad > 0 else ''
    # Quitar 'de ' si queda en el nombre
    if nombre.lower().startswith('de '):
        nombre = nombre[3:].strip()
    return {'cantidad': cantidad, 'unidad': unidad, 'nombre': nombre}


def parsear_ingredientes(texto: str) -> list[dict]:
    """Extrae y parsea todas las líneas de ingredientes de un texto.

    - Detecta líneas con o sin viñeta, con indentación.
    - Incluye ingredientes sin cantidad (p.ej. 'sal al gusto').
    - Se detiene ante secciones de Pasos/Preparación/Notas.
    """
    lines = [l.strip() for l in texto.splitlines()]
    # Buscar cabecera de ingredientes
    start = next((i for i, l in enumerate(lines) if _RGX_INGREDIENTES_HEADER.match(l)), None)
    if start is None:
        return []
    ingredientes = []
    for l in lines[start+1:]:
        # Se detiene al encontrar preparación o notas
        if _RGX_PREPARACION_HEADER.match(l) or _RGX_NOTAS_HEADER.match(l):
            break
        # Saltar líneas vacías sin cortar el bloque
        if not l:
            continue
        # Limpiar sólo viñetas y espacios
        clean = re.sub(r'^[-*\s]+', '', l)
        parsed = parsear_linea_ingrediente(clean)
        if parsed['nombre']:
            ingredientes.append(parsed)
    return ingredientes


def extraer_nombre(texto: str) -> str:
    for l in texto.splitlines():
        if l.strip():
            return l.strip()
    return 'Desconocido'


def extraer_url_origen(texto: str) -> str:
    m = _RGX_URL.search(texto)
    return m.group(0) if m else 'Desconocido'


def extraer_porciones(texto: str) -> int | str:
    m = _RGX_PORCIONES.search(texto)
    return int(m.group(1)) if m else 'Desconocido'


def extraer_calorias(texto: str) -> int | str:
    m = _RGX_CALORIAS.search(texto)
    return int(m.group(1)) if m else 'Desconocido'


def extraer_preparacion(texto: str) -> list[str]:
    """Extrae sección de preparación en lista de pasos completos."""
    lines = [l.strip() for l in texto.splitlines()]
    start = next((i for i, l in enumerate(lines) if _RGX_PREPARACION_HEADER.match(l)), None)
    if start is None:
        return []
    pasos = []
    buffer = ''
    for l in lines[start+1:]:
        if not l or _RGX_NOTAS_HEADER.match(l):
            break
        m = re.match(r'^(\d+)\.?\s*(.*)', l)
        if m:
            if buffer:
                pasos.append(buffer.strip())
            buffer = m.group(2).strip()
        else:
            buffer += ' ' + l
    if buffer:
        pasos.append(buffer.strip())
    return pasos


def normalizar_receta_desde_texto(texto: str) -> dict:
    return {
        'nombre': extraer_nombre(texto),
        'url_origen': extraer_url_origen(texto),
        'porciones': extraer_porciones(texto),
        'calorias_totales': extraer_calorias(texto),
        'ingredientes': parsear_ingredientes(texto),
        'preparacion': extraer_preparacion(texto),
    }
