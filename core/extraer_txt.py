"""
Módulo para extraer texto de archivos de texto plano.

Maneja la lectura de archivos .txt con diferentes codificaciones.
"""

from pathlib import Path
import tempfile
import os
import unicodedata

from core.config import ENCODING_DEFAULT
from core.logger import configurar_logger, log_error

logger = configurar_logger("extraer_txt")


def _es_archivo_binario(content: bytes) -> bool:
    """
    Determina si un archivo es binario basado en su contenido.
    
    Utiliza una combinación de heurísticas para detectar archivos binarios:
    1. Presencia de bytes nulos
    2. Alta proporción de bytes no imprimibles
    3. Análisis de la distribución de bytes
    4. Detección de secuencias de escape comunes
    5. Verificación de caracteres de control válidos
    
    Args:
        content: Contenido del archivo en bytes
    
    Returns:
        bool: True si el archivo es binario, False si es texto
    """
    # Si está vacío, no es binario
    if not content:
        return False
        
    # Detecta BOM markers y los ignora para el análisis
    if content.startswith(b'\xef\xbb\xbf'):  # UTF-8 BOM
        content = content[3:]
    elif content.startswith(b'\xff\xfe'):  # UTF-16 LE BOM
        return False
    elif content.startswith(b'\xfe\xff'):  # UTF-16 BE BOM
        return False
    elif content.startswith(b'\x00\x00\xfe\xff'):  # UTF-32 BE BOM
        return False
    elif content.startswith(b'\xff\xfe\x00\x00'):  # UTF-32 LE BOM
        return False
        
    # Toma una muestra del archivo para análisis
    sample = content[:4096] if len(content) > 4096 else content
    
    # Caracteres de control permitidos (comunes en texto)
    allowed_control = {
        9,  # tab
        10, # LF
        13, # CR
        27, # ESC
        7,  # bell
        8,  # backspace
        12, # form feed
        32  # space
    }
    
    # Secuencias de escape comunes en texto
    common_escapes = {
        b'\x1b[',  # ANSI escape sequences
        b'\x1b(',   # VT100 escape sequences
        b'\x1b]',   # OSC sequences
        b'\x1b_'    # APC sequences
    }
    
    # Verifica si hay secuencias de escape válidas
    has_valid_escapes = any(seq in sample for seq in common_escapes)
    
    # Cuenta bytes nulos y calcula su proporción
    null_count = sample.count(b'\x00')
    null_ratio = null_count / len(sample)
    
    # Si hay más de 3 bytes nulos consecutivos, es binario
    for i in range(len(sample) - 3):
        if sample[i:i+4] == b'\x00\x00\x00\x00':
            return True
    
    # Si hay una alta proporción de bytes nulos (>10%), es binario
    if null_ratio > 0.10:
        return True
    
    # Cuenta bytes no imprimibles (excluyendo caracteres de control comunes)
    non_printable = sum(1 for byte in sample 
                       if byte < 32 and byte not in allowed_control)
    non_printable_ratio = non_printable / len(sample)
    
    # Si más del 30% son bytes no imprimibles y no hay secuencias de escape válidas,
    # consideramos que es binario
    if non_printable_ratio > 0.30 and not has_valid_escapes:
        return True
        
    # Analiza la distribución de bytes para detectar patrones binarios
    byte_dist = {}
    for byte in sample:
        byte_dist[byte] = byte_dist.get(byte, 0) + 1
    
    # En texto normal, algunos bytes son mucho más comunes que otros
    # En binario, la distribución tiende a ser más uniforme
    common_bytes = sum(1 for count in byte_dist.values() 
                      if (count / len(sample)) > 0.05)
    
    # Si hay demasiados bytes con frecuencia similar y no hay secuencias de escape válidas,
    # probablemente es binario
    if common_bytes > 8 and not has_valid_escapes:
        return True
        
    # Verifica si hay caracteres de control inválidos
    invalid_control = sum(1 for byte in sample 
                         if byte < 32 and byte not in allowed_control)
    
    # Si hay caracteres de control inválidos y no hay secuencias de escape válidas,
    # probablemente es binario, a menos que sea un solo byte nulo o un carácter de control válido
    if invalid_control > 1 and not has_valid_escapes:
        # Verifica si los caracteres de control son parte de una secuencia de escape válida
        for i in range(len(sample) - 1):
            if sample[i] == 0x1b and i + 1 < len(sample):
                next_byte = sample[i + 1]
                if next_byte in [ord('['), ord('('), ord(']'), ord('_')]:
                    return False
        return True
    elif invalid_control == 1 and not has_valid_escapes and null_count == 0:
        # Verifica si el único carácter de control es un byte nulo o un carácter de control válido
        for byte in sample:
            if byte < 32 and byte not in allowed_control:
                return byte not in [0x00] + list(allowed_control)
        
    # Si llegamos aquí, probablemente es texto
    return False


def extraer_texto_desde_txt(ruta: Path) -> str:
    """
    Extrae texto de un archivo .txt.

    Args:
        ruta: Ruta al archivo de texto

    Returns:
        str: Contenido del archivo de texto
    """
    if not ruta.exists():
        log_error(f"El archivo no existe: {ruta}")
        return ""

    try:
        # Primero lee el archivo como binario para detectar BOM y tipo de archivo
        with open(ruta, 'rb') as f:
            content = f.read()
            
            # Si está vacío, retorna cadena vacía pero solo si el archivo realmente está vacío
            if not content:
                with open(ruta, 'r') as f:
                    if f.read() == "":
                        return ""
            
            # Detecta BOM y decodifica según corresponda
            if content.startswith(b'\xef\xbb\xbf'):  # UTF-8 BOM
                try:
                    text = content[3:].decode('utf-8')
                    return text.replace('\ufeff', '')
                except UnicodeError:
                    pass
            elif content.startswith(b'\xff\xfe\x00\x00'):  # UTF-32 LE BOM
                try:
                    text = content[4:].decode('utf-32-le')
                    return text.replace('\ufeff', '')
                except UnicodeError:
                    pass
            elif content.startswith(b'\x00\x00\xfe\xff'):  # UTF-32 BE BOM
                try:
                    text = content[4:].decode('utf-32-be')
                    return text.replace('\ufeff', '')
                except UnicodeError:
                    pass
            elif content.startswith(b'\xff\xfe'):  # UTF-16 LE BOM
                try:
                    text = content[2:].decode('utf-16-le')
                    return text.replace('\ufeff', '')
                except UnicodeError:
                    pass
            elif content.startswith(b'\xfe\xff'):  # UTF-16 BE BOM
                try:
                    text = content[2:].decode('utf-16-be')
                    return text.replace('\ufeff', '')
                except UnicodeError:
                    pass
            
            # Verifica si es binario antes de intentar decodificar
            if _es_archivo_binario(content):
                return ""
            
            # Si no tiene BOM, intenta con diferentes codificaciones
            encodings = [
                ENCODING_DEFAULT,  # Primero intenta la codificación por defecto
                "utf-8",          # UTF-8 sin BOM
                "latin1",         # Latin-1 (ISO-8859-1)
                "cp1252",         # Windows-1252
                "iso-8859-15",    # Latin-9
                "cp850",          # DOS Latin-1
                "cp852",          # DOS Latin-2
                "ascii",          # ASCII
                "utf-16",         # UTF-16 sin BOM
                "utf-32",         # UTF-32 sin BOM
                "mac_roman",      # Mac Roman
                "cp437",          # DOS/IBM PC
                "cp866",          # DOS Cyrillic
            ]
            
            # Intenta decodificar con cada codificación
            for encoding in encodings:
                try:
                    text = content.decode(encoding)
                    # Remove BOM character if present
                    text = text.replace('\ufeff', '')
                    
                    # Verifica que el texto decodificado sea válido
                    if text and all(ord(c) < 0x10000 or unicodedata.category(c) != 'Cn' for c in text):
                        # Para codificaciones que pueden tener caracteres especiales,
                        # verifica que la decodificación sea consistente
                        if encoding in ['latin1', 'cp1252', 'iso-8859-15', 'cp850', 'cp852']:
                            # Verifica que los caracteres especiales se mantengan
                            special_chars = 'áéíóúñüÁÉÍÓÚÑÜ'
                            if any(c in text for c in special_chars):
                                # Si contiene caracteres especiales, verifica que se mantengan
                                test_encode = text.encode(encoding)
                                test_decode = test_encode.decode(encoding)
                                if test_decode != text:
                                    continue
                        return text
                except UnicodeError:
                    continue
            
            # Si ninguna codificación funciona, intenta una decodificación más permisiva
            try:
                # Intenta decodificar ignorando errores
                text = content.decode('utf-8', errors='replace')
                # Remove BOM character if present
                return text.replace('\ufeff', '')
            except UnicodeError:
                log_error(f"No se pudo determinar la codificación de {ruta}")
                return ""
    except Exception as e:
        log_error(f"Error al leer {ruta}: {e}")
        return ""


def _leer_archivo_temporal(ruta: Path) -> str:
    """
    Lee un archivo temporal, asegurándose de que se cierre correctamente.

    Args:
        ruta: Ruta al archivo temporal

    Returns:
        str: Contenido del archivo
    """
    try:
        # Primero intenta leer como texto
        try:
            with open(ruta, 'r', encoding=ENCODING_DEFAULT) as f:
                return f.read()
        except UnicodeError:
            # Si falla, intenta leer como binario
            with open(ruta, 'rb') as f:
                content = f.read()
                # Intenta detectar el BOM
                if content.startswith(b'\xef\xbb\xbf'):  # UTF-8 BOM
                    return content[3:].decode('utf-8')
                elif content.startswith(b'\xff\xfe'):  # UTF-16 LE BOM
                    return content[2:].decode('utf-16-le')
                elif content.startswith(b'\xfe\xff'):  # UTF-16 BE BOM
                    return content[2:].decode('utf-16-be')
                else:
                    # Si no hay BOM, intenta con diferentes codificaciones
                    for encoding in [ENCODING_DEFAULT, "utf-8", "latin1", "cp1252"]:
                        try:
                            return content.decode(encoding)
                        except UnicodeError:
                            continue
                    return ""
    except Exception as e:
        log_error(f"Error al leer archivo temporal {ruta}: {e}")
        return ""
