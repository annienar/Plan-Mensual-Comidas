from typing import List, Dict, Any
from .base import BaseExtractor
import re
from fractions import Fraction

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

def _to_float(qty_str: str) -> float:
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

def _parsear_linea_ingrediente(linea: str) -> dict:
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

class IngredientExtractor(BaseExtractor):
    def extract(self, ingredients_text: str) -> List[Dict[str, Any]]:
        """Extract structured ingredient data from text."""
        lines = [l.strip() for l in ingredients_text.splitlines() if l.strip()]
        ingredientes = []
        for l in lines:
            clean = re.sub(r"^[-*\s]+", "", l)
            # Skip lines that are likely instructions or not ingredients
            if re.match(r"^(\.|\d+\.|instrucciones?:|pasos?:|preparaci[oó]n:|steps?:|instructions?:)", clean, re.IGNORECASE):
                continue
            # Remove parenthetical weights (e.g., (120g))
            clean = re.sub(r"\([^)]*\)", "", clean).strip()
            # Remove 'Opcional:' or similar prefixes
            optional = False
            if re.match(r"^(opcional:|opcional -|opcional )", clean, re.IGNORECASE):
                clean = re.sub(r"^(opcional:|opcional -|opcional )", "", clean, flags=re.IGNORECASE).strip()
                optional = True
            parsed = _parsear_linea_ingrediente(clean)
            # Remove 'al gusto' or 'to taste' from the end of the name
            for phrase in ["al gusto", "to taste"]:
                if parsed["nombre"].lower().endswith(phrase):
                    parsed["nombre"] = parsed["nombre"][: -len(phrase)].strip()
            # Remove leading 'de', 'la', 'el', etc.
            parsed["nombre"] = re.sub(r"^(de|la|el|los|las|un|una|unos|unas)\s+", "", parsed["nombre"], flags=re.IGNORECASE)
            # Mark as optional if detected
            if optional:
                parsed["opcional"] = True
            # Split on ' y ' if present in the name
            if " y " in parsed["nombre"]:
                parts = [p.strip() for p in parsed["nombre"].split(" y ")]
                for part in parts:
                    if part:
                        new_parsed = parsed.copy()
                        new_parsed["nombre"] = part
                        ingredientes.append(new_parsed)
            else:
                ingredientes.append(parsed)
        return ingredientes 