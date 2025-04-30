from core.logger import configurar_logger, log_info, log_warning, log_error
logger = configurar_logger("extraer_txt")

def extraer_texto_desde_txt(path_txt):
    texto = ""
    try:
        with open(path_txt, "r", encoding="utf-8") as f:
            texto = f.read().strip()
            log_info(f"📄 Texto extraído correctamente de {path_txt}")
    except Exception as e:
        log_error(f"❌ Error al leer {path_txt}: {e}")
    return texto
