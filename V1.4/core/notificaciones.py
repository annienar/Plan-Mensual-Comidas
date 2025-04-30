"""
core/notificaciones.py
Helpers semánticos que envuelven al logger.

🔸 Deja al logger puro
🔸 Un solo punto para cambiar emojis / textos
"""

from core.logger import log_info, log_warning, log_error

# ------------------------------------------------------------------
# Acciones de sistema de archivos
# ------------------------------------------------------------------
def log_creacion_carpeta(path: str):
    log_info(f"📁 Carpeta creada: {path}")

def log_movimiento_archivo(src: str, dst: str):
    log_info(f"📦 Archivo movido: {src} → {dst}")

def log_creacion_archivo(path: str):
    log_info(f"✅ Archivo creado: {path}")


# ------------------------------------------------------------------
# Otros ejemplos futuros
# ------------------------------------------------------------------
def log_receta_normalizada(nombre: str):
    log_info(f"🍴 Receta normalizada correctamente: {nombre}")

# --- NUEVOS helpers de dominio -----------------------------------
def log_error_archivo(path: str, detalle: str):
    """Error procesando un archivo concreto"""
    log_error(f"❌ Error con archivo {path}: {detalle}")

# ------------------------------------------------------------------
# Aviso de carpeta vacía
# ------------------------------------------------------------------
def log_carpeta_vacia(ruta: str):
    msg = f"⚠️  No se encontraron archivos para procesar en: {ruta}"
    log_warning(msg)
