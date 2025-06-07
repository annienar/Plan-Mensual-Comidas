from typing import List, Dict, Any
import re

from .base import BaseExtractor
from fractions import Fraction
_UNIDADES = {'g': 'g', 'gr': 'g', 'gramo': 'g', 'gramos': 'g', 'kg': 'kg', 
    'ml': 'ml', 'l': 'l', 'taza': 'taza', 'tazas': 'taza', 'cucharada':
    'cucharadas', 'cucharadas': 'cucharadas', 'cda': 'cucharadas', 'cdas':
    'cucharadas', 'cdta': 'cdta', 'tsp': 'cdta', 'cucharadita': 'cdta', 
    'cucharaditas': 'cdta'}

def _to_float(qty_str: str) -> float:
    """Function _to_float."""
    s = qty_str.strip().lower()
    
    # Handle unicode fractions first
    unicode_fractions = {
        '½': 0.5, '¼': 0.25, '¾': 0.75, '⅓': 0.333, '⅔': 0.667,
        '⅛': 0.125, '⅜': 0.375, '⅝': 0.625, '⅞': 0.875
    }
    
    # Check for mixed unicode fractions (e.g., "1½", "2¼")
    for unicode_char, decimal_val in unicode_fractions.items():
        if unicode_char in s:
            # Replace with space-separated format for mixed numbers
            s = s.replace(unicode_char, f' {decimal_val}')
    
    # Take first part if there are ranges/alternatives
    raw = re.split('–|-|\\bo\\b', s)[0].strip()
    
    # Handle mixed fractions (e.g., "1 1/2" or "1 0.5")
    mixed_match = re.match(r'^(\d+)\s+(\d+)/(\d+)$', raw)
    if mixed_match:
        whole = int(mixed_match.group(1))
        numerator = int(mixed_match.group(2))
        denominator = int(mixed_match.group(3))
        return whole + numerator / denominator
    
    # Handle mixed decimal (e.g., "1 0.5")  
    mixed_decimal_match = re.match(r'^(\d+)\s+(\d*\.\d+)$', raw)
    if mixed_decimal_match:
        whole = int(mixed_decimal_match.group(1))
        decimal_part = float(mixed_decimal_match.group(2))
        return whole + decimal_part
    
    # Handle regular fractions (e.g., "1/2")
    if '/' in raw:
        try:
            return float(Fraction(raw))
        except Exception:
            pass
    
    # Handle regular numbers
    try:
        return float(raw)
    except Exception:
        return 0.0

def _parsear_linea_ingrediente(linea: str) -> dict:
    """Function _parsear_linea_ingrediente."""
    text = linea.strip()
    # Try to match quantity patterns: fractions, mixed numbers, decimals, integers, unicode fractions
    m = re.match(r'^(\d+(?:\s+\d+/\d+)?|\d*/\d+|\d+(?:\.\d+)?|.*?[½¼¾⅓⅔⅛⅜⅝⅞])(?:\s*(?:–|-|o)\s*\d+)?\s+(.*)$', text, re.IGNORECASE)
    if not m:
        # Fallback: try simpler patterns
        m = re.match(r'^([0-9½¼¾⅓⅔⅛⅜⅝⅞/.\s]+)\s+(.*)$', text, re.IGNORECASE)
    if m:
        raw_qty, resto = m.groups()
        cantidad = _to_float(raw_qty)
    else:
        cantidad = 0.0
        resto = text
    resto = resto.strip()
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
    if nombre.lower().startswith('de '):
        nombre = nombre[3:].strip()
    return {'cantidad': cantidad, 'unidad': unidad, 'nombre': nombre}

class IngredientExtractor(BaseExtractor):
    """Class IngredientExtractor."""

    def extract(self: Any, ingredients_text: str) ->List[Dict[str, Any]]:
        """Extract structured ingredient data from text."""
        lines = [l.strip() for l in ingredients_text.splitlines() if l.strip()]
        ingredientes = []
        for l in lines:
            clean = re.sub(r'^[-*\s]+', '', l)
            if re.match(r'^(\.|\d+\.|instrucciones?:|pasos?:|preparaci[oó]n:|steps?:|instructions?:)', clean, re.IGNORECASE):
                continue
            clean = re.sub(r'\([^)]*\)', '', clean).strip()
            optional = False
            if re.match('^(opcional:|opcional -|opcional)', clean, re.IGNORECASE):
                clean = re.sub('^(opcional:|opcional -|opcional)', '', clean, flags = re.IGNORECASE).strip()
                optional = True
            parsed = _parsear_linea_ingrediente(clean)
            for phrase in ['al gusto', 'to taste']:
                if parsed['nombre'].lower().endswith(phrase):
                    parsed['nombre'] = parsed['nombre'][:-len(phrase)].strip()
            parsed['nombre'] = re.sub(r'^(de|la|el|los|las|un|una|unos|unas)\s+', '', parsed['nombre'], flags = re.IGNORECASE)
            if optional:
                parsed['opcional'] = True
            if ' y ' in parsed['nombre']:
                parts = [p.strip() for p in parsed['nombre'].split(' y ')]
                for part in parts:
                    if part:
                        new_parsed = parsed.copy()
                        new_parsed['nombre'] = part
                        ingredientes.append(new_parsed)
            else:
                ingredientes.append(parsed)
        return ingredientes
