# core/generar_md.py
"""Generación de vistas Markdown para las recetas procesadas."""

import json
import os
from fractions import Fraction
from typing import Dict, Union

from core.logger import log_info
from core.notificaciones import log_creacion_archivo, log_creacion_carpeta


def generar_md_todas() -> bool:
    """Genera archivos Markdown para todas las recetas procesadas.

    Lee todos los JSON en recetas/procesadas/Recetas JSON y genera un archivo
    Markdown equivalente en Recetas MD.

    Returns:
        bool: True si se generaron los archivos correctamente
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    json_dir = os.path.join(base_dir, "recetas", "procesadas", "Recetas JSON")
    md_dir = os.path.join(base_dir, "recetas", "procesadas", "Recetas MD")

    # 1. Si no existe la carpeta de JSON, no hay nada que hacer
    if not os.path.isdir(json_dir):
        log_info(f"⚠️ No se encontró carpeta JSON: {json_dir}")
        return True

    # 2. Crear carpeta MD si hace falta
    if not os.path.isdir(md_dir):
        os.makedirs(md_dir, exist_ok=True)
        log_creacion_carpeta(md_dir)

    # Mapeo para singularizar unidades
    plural_to_singular = {
        "tazas": "taza",
        "cucharadas": "cucharada",
        "cucharaditas": "cucharadita",
    }

    # Helper para formatear ingredientes
    def _format_cantidad_unidad(ing: Dict[str, Union[float, str]]) -> str:
        """
        Formatea un ingrediente para su visualización en Markdown.

        Args:
            ing: Diccionario con los datos del ingrediente

        Returns:
            str: Línea formateada del ingrediente
        """
        c = float(ing.get("cantidad", 0))
        u = str(ing.get("unidad", ""))
        n = str(ing.get("nombre", "")).lower().split(",")[0].strip()
        # Sin cantidad (ej. 'sal al gusto')
        if not c:
            return f"- {n}"
        # Convertir decimal a fracción mixta o entero
        if c.is_integer():
            qty = str(int(c))
        else:
            frac = Fraction(c).limit_denominator()
            if frac.denominator == 1:
                qty = str(frac.numerator)
            elif frac.numerator > frac.denominator:
                whole = frac.numerator // frac.denominator
                rem = frac.numerator - whole * frac.denominator
                qty = f"{whole} {rem}/{frac.denominator}"
            else:
                qty = f"{frac.numerator}/{frac.denominator}"
        # Singularizar unidad si qty == 1
        if u in plural_to_singular and qty == "1":
            u = plural_to_singular[u]
        # Formatear línea
        if u and u != "u":
            return f"- {qty} {u} de {n}"
        else:
            return f"- {qty} {n}"

    # 3. Procesar cada JSON
    try:
        for fname in os.listdir(json_dir):
            if not fname.lower().endswith(".json"):
                continue
            path_json = os.path.join(json_dir, fname)
            with open(path_json, "r", encoding="utf-8") as f:
                receta = json.load(f)

            # Valores por defecto y separación de título/autor
            raw_name = receta.get("nombre", "Desconocido")
            if "Receta de " in raw_name:
                main_title, author = raw_name.split("Receta de ", 1)
                author_text = author.strip()
                title = main_title.strip()
            else:
                title = raw_name
                author_text = None
            por_val = receta.get("porciones", 0)
            porciones = (
                por_val if isinstance(por_val, int) and por_val > 0 else "Desconocido"
            )
            cal_val = receta.get("calorias_totales", 0)
            calorias = (
                cal_val if isinstance(cal_val, int) and cal_val > 0 else "Desconocido"
            )
            origen = receta.get("url_origen") or "Desconocido"

            # Nombre del MD de salida
            md_name = os.path.splitext(fname)[0] + ".md"
            path_md = os.path.join(md_dir, md_name)

            with open(path_md, "w", encoding="utf-8") as f_md:
                # Título y autor opcional
                f_md.write(f"# {title}\n\n")
                if author_text:
                    f_md.write(f"*Receta de {author_text}*\n\n")
                # Metadatos
                f_md.write(f"- **Porciones:** {porciones}\n")
                f_md.write(f"- **Calorías totales:** {calorias}\n")
                f_md.write(f"- **Origen:** {origen}\n\n")

                # Ingredientes
                f_md.write("## Ingredientes\n")
                for ing in receta.get("ingredientes", []):
                    f_md.write(_format_cantidad_unidad(ing) + "\n")
                f_md.write("\n")

                # Preparación
                f_md.write("## Preparación\n")
                for idx, paso in enumerate(receta.get("preparacion", []), 1):
                    f_md.write(f"{idx}. {paso}\n")

            log_creacion_archivo(path_md)
            log_info(f"✅ Markdown generado: {path_md}")
        return True
    except Exception as e:
        log_info(f"❌ Error al generar Markdown: {e}")
        return False
