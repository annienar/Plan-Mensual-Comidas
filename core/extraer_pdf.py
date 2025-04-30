# core/extraer_pdf.py
# ---------------------------------------------------
# Extracción robusta de texto desde PDFs (v1.4.9)
#  - Usa pdfplumber con tolerancias para respetar saltos
#  - Elimina menús, footers y enlaces ruidosos
#  - Repara guiones de fin de línea y une páginas
# ---------------------------------------------------

import re
import logging
import pdfplumber
from core.logger import configurar_logger, log_info, log_warning, log_error

# Suprime logs excesivos de pdfminer
logging.getLogger("pdfminer").setLevel(logging.ERROR)

# Inicializa logger del módulo
logger = configurar_logger("extraer_pdf")


def extraer_texto_desde_pdf(path_pdf: str) -> str:
    """
    Devuelve el texto limpio del PDF en `path_pdf`, listo para parsear ingredientes.

    - Concatena todas las páginas con doble salto de línea.
    - Elimina URLs, protocolos whatsapp://, javascript:, etc.
    - Suprime bloques de navegación/footers de la web.
    - Repara palabras rotas por guión al final de línea.
    - Loggea éxito o error.
    """
    paginas: list[str] = []
    try:
        with pdfplumber.open(path_pdf) as pdf:
            for page in pdf.pages:
                # extrae texto conservando saltos de párrafo
                txt = page.extract_text(x_tolerance=1, y_tolerance=3) or ""
                paginas.append(txt.strip())
        bruto = "\n\n=== página ===\n\n".join(paginas)
        log_info(f"📄 Texto extraído correctamente de {path_pdf}")
    except Exception as e:
        log_error(f"❌ Error al leer {path_pdf}: {e}")
        return ""

    # ── Limpieza de enlaces y protocolos no deseados ─────────────────────
    limpio = re.sub(r"https?://\S+|whatsapp://\S+|javascript:\S+", "", bruto)

    # ── Suprime bloques de navegación/footers repetitivos ───────────────
    patrones_ruido = [
        r"© COPYRIGHT.*?DERECHOS RESERVADOS",          # footer legal
        r"Síguenos.*?Resumen de votos",                # sección social
        r"PORTADA\s+RECETAS[\s\S]{0,400}?Bon Viveur",  # cabecera de web BonViveur
    ]
    for pat in patrones_ruido:
        limpio = re.sub(pat, "", limpio, flags=re.I | re.S)

    # ── Normaliza espacios y tabs ────────────────────────────────────────
    limpio = re.sub(r"[ \t]+", " ", limpio)

    # ── Repara palabras partidas por guión al final de línea ────────────
    limpio = re.sub(r"(\w+)-\n(\w+)", r"\1\2", limpio)

    # ── Colapsa saltos de línea múltiples ────────────────────────────────
    limpio = re.sub(r"\n{3,}", "\n\n", limpio).strip()

    return limpio
