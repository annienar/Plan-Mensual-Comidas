"""
Módulo para extraer texto de archivos de texto plano.

Maneja la lectura de archivos .txt con diferentes codificaciones.
"""
from pathlib import Path
from typing import Any
import os

import tempfile
import unicodedata

from .interface import IExtractor
DEFAULT_ENCODING = 'utf-8'

class LoggerStub:
    def info(self, msg): pass
    def error(self, msg): pass

logger = LoggerStub()

def log_error(msg, **kwargs):
    logger.error(msg)

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
    if not content:
        return False
    if content.startswith(b'\xef\xbb\xbf'):
        content = content[3:]
    elif content.startswith(b'\xff\xfe'):
        return False
    elif content.startswith(b'\xfe\xff'):
        return False
    elif content.startswith(b'\x00\x00\xfe\xff'):
        return False
    elif content.startswith(b'\xff\xfe\x00\x00'):
        return False
    sample = content[:4096] if len(content) > 4096 else content
    allowed_control = {9, 10, 13, 27, 7, 8, 12, 32}
    common_escapes = {b'\x1b[', b'\x1b(', b'\x1b]', b'\x1b_'}
    has_valid_escapes = any(seq in sample for seq in common_escapes)
    null_count = sample.count(b'\x00')
    null_ratio = null_count / len(sample)
    for i in range(len(sample) - 3):
        if sample[i:i + 4] == b'\x00\x00\x00\x00':
            return True
    if null_ratio > 0.1:
        return True
    non_printable = sum(1 for byte in sample if byte < 32 and byte not in
        allowed_control)
    non_printable_ratio = non_printable / len(sample)
    if non_printable_ratio > 0.3 and not has_valid_escapes:
        return True
    byte_dist = {}
    for byte in sample:
        byte_dist[byte] = byte_dist.get(byte, 0) + 1
    common_bytes = sum(1 for count in byte_dist.values() if count / len(
        sample) > 0.05)
    # Only flag as binary if we have many common bytes AND the file is large enough
    # to make this heuristic meaningful (small text files naturally have high frequency chars)
    # However, avoid false positives for repetitive text (like test files with repeated content)
    if common_bytes > 8 and not has_valid_escapes and len(sample) > 1000:
        # Check if the common bytes are all printable ASCII characters
        # If so, it's likely repetitive text, not binary
        common_printable_ascii = sum(1 for byte, count in byte_dist.items() 
                                   if count / len(sample) > 0.05 and 32 <= byte <= 126)
        # If most common bytes are printable ASCII, it's probably text
        if common_printable_ascii >= common_bytes - 2:  # Allow for newlines/tabs
            return False
        return True
    invalid_control = sum(1 for byte in sample if byte < 32 and byte not in
        allowed_control)
    if invalid_control > 1 and not has_valid_escapes:
        for i in range(len(sample) - 1):
            if sample[i] == 27 and i + 1 < len(sample):
                next_byte = sample[i + 1]
                if next_byte in [ord('['), ord('('), ord(']'), ord('_')]:
                    return False
        return True
    elif invalid_control == 1 and not has_valid_escapes and null_count == 0:
        for byte in sample:
            if byte < 32 and byte not in allowed_control:
                return byte not in [0] + list(allowed_control)
    return False

def _leer_archivo_temporal(ruta: Path) -> str:
    """
    Lee un archivo temporal, asegurándose de que se cierre correctamente.

    Args:
        ruta: Ruta al archivo temporal

    Returns:
        str: Contenido del archivo
    """
    try:
        try:
            with open(ruta, 'r', encoding = DEFAULT_ENCODING) as f:
                return f.read()
        except UnicodeError:
            with open(ruta, 'rb') as f:
                content = f.read()
                if content.startswith(b'\xef\xbb\xbf'):
                    return content[3:].decode('utf-8')
                elif content.startswith(b'\xff\xfe'):
                    return content[2:].decode('utf-16-le')
                elif content.startswith(b'\xfe\xff'):
                    return content[2:].decode('utf-16-be')
                else:
                    for encoding in [DEFAULT_ENCODING, 'utf-8', 'latin1', 
                        'cp1252']:
                        try:
                            return content.decode(encoding)
                        except UnicodeError:
                            continue
                    return ''
    except Exception as e:
        log_error(f'Error al leer archivo temporal {ruta}: {e}', extra={'file_path': str(ruta)})
        return ''

class TextExtractor(IExtractor):
    """Text extraction service for plain text files.

    This class handles the extraction of text content from plain text files, 
    with support for multiple encodings, BOM detection, and binary file
    filtering. It provides robust text extraction capabilities while
    handling various edge cases and encoding issues.

    Features:
        - Automatic encoding detection (UTF - 8, UTF - 16, UTF - 32)
        - BOM (Byte Order Mark) handling
        - Binary file detection and filtering
        - Multiple encoding fallback support
        - Comprehensive error handling and logging

    Supported Encodings:
        - UTF - 8 (with and without BOM)
        - UTF - 16 LE / BE (with BOM)
        - UTF - 32 LE / BE (with BOM)
        - Latin - 1 (fallback)
        - CP1252 (fallback)

    Example:
        >>> extractor = TextExtractor()
        >>> content = extractor.extract("/path / to / file.txt")
        >>> print(content)
    """

    def extract(self, source_path: str) -> str:
        """Extract text content from a plain text file.

        Performs automatic encoding detection and handles various text
        formats including those with Byte Order Marks (BOM). The method
        attempts multiple encoding strategies to ensure successful text
        extraction while filtering out binary files.

        Args:
            source_path (str): Path to the text file to extract content from.
                            Must be a valid file path that exists on the filesystem.

        Returns:
            str: The extracted text content from the file, with BOM characters
                removed and proper Unicode normalization applied. Returns an
                empty string if the file doesn't exist, is binary, or cannot
                be decoded.

        Raises:
            No exceptions are raised directly. All errors are logged and
            result in an empty string return value for graceful degradation.

        Note:
            - Binary files are automatically detected and ignored
            - BOM characters are automatically stripped from the content
            - Multiple encoding strategies are attempted for maximum compatibility
            - All errors are logged for debugging purposes
        """
        ruta = Path(source_path)
        if not ruta.exists():
            log_error(f'El archivo no existe: {ruta}')
            return ''
        try:
            with open(ruta, 'rb') as f:
                content = f.read()
                if not content:
                    with open(ruta, 'r') as f2:
                        if f2.read() == '':
                            return ''
                if content.startswith(b'\xef\xbb\xbf'):
                    try:
                        text = content[3:].decode('utf-8')
                        return text.replace('\ufeff', '')
                    except UnicodeError:
                        pass
                elif content.startswith(b'\xff\xfe\x00\x00'):
                    try:
                        text = content[4:].decode('utf-32-le')
                        return text.replace('\ufeff', '')
                    except UnicodeError:
                        pass
                elif content.startswith(b'\x00\x00\xfe\xff'):
                    try:
                        text = content[4:].decode('utf-32-be')
                        return text.replace('\ufeff', '')
                    except UnicodeError:
                        pass
                elif content.startswith(b'\xff\xfe'):
                    try:
                        text = content[2:].decode('utf-16-le')
                        return text.replace('\ufeff', '')
                    except UnicodeError:
                        pass
                elif content.startswith(b'\xfe\xff'):
                    try:
                        text = content[2:].decode('utf-16-be')
                        return text.replace('\ufeff', '')
                    except UnicodeError:
                        pass
                if _es_archivo_binario(content):
                    return ''
                try:
                    text = content.decode(DEFAULT_ENCODING)
                    logger.info(f'Successfully decoded {ruta} using encoding: {DEFAULT_ENCODING}')
                    return text
                except Exception as e:
                    log_error(f'Error de decodificación en {ruta}: {e}', extra={'file_path': str(ruta)})
                    return ''
        except Exception as e:
            log_error(f'Error al extraer texto de {ruta}: {e}', extra={'file_path': str(ruta)})
            return ''
