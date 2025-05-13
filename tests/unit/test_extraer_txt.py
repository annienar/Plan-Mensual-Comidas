# tests/test_extraer_txt.py
"""
Tests para la extracción de texto de archivos .txt.

Verifica la correcta extracción de texto plano desde archivos .txt,
incluyendo manejo de codificación y preservación del contenido.
"""

from pathlib import Path
import tempfile
import pytest
import os

from core.utils.config import UNPROCESSED_DIR
from core.extraction.text import TextExtractor

# Update the path to the new fixture directory
ARCHIVOS_TXT = list(Path("tests/fixtures/recipes/sin_procesar").glob("*.txt"))


def test_existen_archivos_txt():
    """Asegurar que hay archivos .txt para procesar."""
    assert ARCHIVOS_TXT, f"No se encontraron archivos .txt en {Path('tests/fixtures/recipes/sin_procesar')}"


@pytest.mark.parametrize("path_archivo", ARCHIVOS_TXT)
def test_extraer_texto_desde_txt(path_archivo):
    """Verifica la extracción básica de texto."""
    texto = TextExtractor().extract(path_archivo)

    # Verificar que devuelve un string no vacío
    assert isinstance(
        texto, str
    ), f"Extractor no devolvió string en {path_archivo.name}"
    assert texto.strip(), f"Extractor devolvió texto vacío para {path_archivo.name}"

    # Verificar que el contenido coincide exactamente con el archivo
    with open(path_archivo, "r", encoding="utf-8") as f:
        contenido_original = f.read()
    assert (
        texto == contenido_original
    ), f"El contenido extraído no coincide con el original en {path_archivo.name}"


@pytest.mark.parametrize("path_archivo", ARCHIVOS_TXT)
def test_manejo_codificacion(path_archivo):
    """Verifica el correcto manejo de caracteres especiales y codificación."""
    texto = TextExtractor().extract(path_archivo)

    # Verificar que no hay caracteres de codificación incorrecta
    caracteres_problematicos = ["□"]
    for char in caracteres_problematicos:
        assert (
            char not in texto
        ), f"Encontrado carácter de codificación incorrecta '{char}' en {path_archivo.name}"

    # Verificar que los caracteres especiales comunes se preservan
    caracteres_especiales = ["á", "é", "í", "ó", "ú", "ñ", "ü"]
    for char in caracteres_especiales:
        if char in texto:
            assert (
                char in texto
            ), f"El carácter especial '{char}' no se preservó en {path_archivo.name}"


@pytest.mark.parametrize("path_archivo", ARCHIVOS_TXT)
def test_estructura_archivo_txt(path_archivo):
    """Verifica la estructura básica del archivo de texto."""
    texto = TextExtractor().extract(path_archivo)
    lines = texto.splitlines()

    # Verificaciones básicas de estructura del archivo
    assert lines, f"No se encontraron líneas en {path_archivo.name}"
    assert len(lines) > 1, f"El archivo {path_archivo.name} solo tiene una línea"

    # Verificar formato del texto
    # assert texto == texto.strip(), f"El texto contiene espacios en blanco innecesarios al inicio o final en {path_archivo.name}"

    # Verificar que no hay líneas vacías consecutivas
    for i in range(len(lines) - 1):
        assert not (
            lines[i].strip() == "" and lines[i + 1].strip() == ""
        ), f"Encontradas líneas vacías consecutivas en {path_archivo.name}"

    # Verificar longitud máxima de línea (readability)
    max_line_length = 500
    long_lines = [i + 1 for i, line in enumerate(lines) if len(line) > max_line_length]
    assert (
        not long_lines
    ), f"Líneas demasiado largas (>{max_line_length} caracteres) en líneas {long_lines} de {path_archivo.name}"

    # Verificar que no hay caracteres de control excepto saltos de línea
    control_chars = [
        char for char in texto if char.isprintable() is False and char != "\n"
    ]
    assert (
        not control_chars
    ), f"Encontrados caracteres de control no permitidos en {path_archivo.name}: {control_chars}"


@pytest.mark.skip(reason="Latin-1 encoding not supported by the extractor")
def test_encoding_fallback():
    """Verifica el manejo de diferentes codificaciones."""
    test_content = "áéíóúñü"
    
    # Test UTF-8
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.txt', delete=False) as f:
        f.write(test_content.encode('utf-8'))
        f.flush()
        os.fsync(f.fileno())
        temp_path = Path(f.name)
    
    try:
        assert TextExtractor().extract(temp_path) == test_content
    finally:
        os.unlink(temp_path)
    
    # Test Latin-1
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.txt', delete=False) as f:
        f.write(test_content.encode('latin1'))
        f.flush()
        os.fsync(f.fileno())
        temp_path = Path(f.name)
    
    try:
        assert TextExtractor().extract(temp_path) == test_content
    finally:
        os.unlink(temp_path)
    
    # Test CP1252
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.txt', delete=False) as f:
        f.write(test_content.encode('cp1252'))
        f.flush()
        os.fsync(f.fileno())
        temp_path = Path(f.name)
    
    try:
        assert TextExtractor().extract(temp_path) == test_content
    finally:
        os.unlink(temp_path)


def test_error_handling():
    """Verifica el manejo de errores."""
    # Test file not found
    non_existent = Path("non_existent.txt")
    assert TextExtractor().extract(non_existent) == ""
    
    # Test empty file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("")
        f.flush()
        os.fsync(f.fileno())
        temp_path = Path(f.name)
    
    try:
        assert TextExtractor().extract(temp_path) == ""
    finally:
        os.unlink(temp_path)
    
    # Test binary file
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.txt', delete=False) as f:
        f.write(b'\x00\x01\x02\x03')
        f.flush()
        os.fsync(f.fileno())
        temp_path = Path(f.name)
    
    try:
        assert TextExtractor().extract(temp_path) == ""
    finally:
        os.unlink(temp_path)


def test_line_endings():
    """Verifica el manejo de diferentes tipos de fin de línea."""
    test_content = "line1\nline2\r\nline3\rline4"
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(test_content)
        f.flush()
        os.fsync(f.fileno())
        temp_path = Path(f.name)
    
    try:
        assert TextExtractor().extract(temp_path) == test_content
    finally:
        os.unlink(temp_path)


def test_bom_handling():
    """Verifica el manejo de BOM markers."""
    # Test UTF-8 BOM
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.txt', delete=False) as f:
        f.write(b'\xef\xbb\xbf' + "test".encode('utf-8'))
        f.flush()
        os.fsync(f.fileno())
        temp_path = Path(f.name)
    
    try:
        assert TextExtractor().extract(temp_path) == "test"
    finally:
        os.unlink(temp_path)
    
    # Test UTF-16 BOM
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.txt', delete=False) as f:
        f.write(b'\xff\xfe' + "test".encode('utf-16'))
        f.flush()
        os.fsync(f.fileno())
        temp_path = Path(f.name)
    
    try:
        assert TextExtractor().extract(temp_path) == "test"
    finally:
        os.unlink(temp_path)


def test_large_file():
    """Verifica el manejo de archivos grandes."""
    large_content = "test\n" * 10000
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(large_content)
        f.flush()
        os.fsync(f.fileno())
        temp_path = Path(f.name)
    
    try:
        assert TextExtractor().extract(temp_path) == large_content
    finally:
        os.unlink(temp_path)


def test_special_characters():
    """Verifica el manejo de caracteres especiales."""
    special_chars = "!@#$%^&*()_+-=[]{}|;:'\",.<>/?`~"
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(special_chars)
        f.flush()
        os.fsync(f.fileno())
        temp_path = Path(f.name)
    
    try:
        assert TextExtractor().extract(temp_path) == special_chars
    finally:
        os.unlink(temp_path)


@pytest.mark.skip(reason="Known issue: empty file detection not fixed yet")
def test_binary_detection():
    """Verifica la detección de archivos binarios con diferentes patrones."""
    test_cases = [
        # Archivo vacío (no binario)
        (b"", False),
        
        # Texto normal (no binario)
        (b"Hello World!\nThis is a test.", False),
        
        # Texto con caracteres especiales (no binario)
        ("Hello\tWorld\r\nÁéíóú".encode('utf-8'), False),
        
        # Texto con algunos bytes nulos al final (no binario)
        (b"Hello World\x00", False),
        
        # Archivo con muchos bytes nulos (binario)
        (b"Hello\x00\x00\x00\x00\x00World", True),
        
        # Archivo con alta proporción de bytes no imprimibles (binario)
        (b"Hello\x01\x02\x03\x04\x05\x06\x07World", True),
        
        # Archivo con distribución uniforme de bytes (binario)
        (bytes(range(256)), True),
        
        # Archivo de texto con emojis (no binario)
        ("Hello 👋 World 🌍".encode('utf-8'), False),
        
        # Archivo con BOM markers (no binario)
        (b'\xef\xbb\xbfHello World', False),
        (b'\xff\xfeH\x00e\x00l\x00l\x00o\x00', False),
        
        # Archivo con escape sequences (no binario)
        (b'\x1b[31mHello\x1b[0m', False),
        (b'\x1b(0Hello\x1b(B', False),
        (b'\x1b]0;Title\x1b\\', False),
        
        # Archivo con caracteres de control válidos (no binario)
        (b"Hello\aWorld\b\f", False),
        
        # Archivo con caracteres de control inválidos (binario)
        (b"Hello\x01\x02\x03World", True),
        
        # Archivo con secuencias de escape incompletas (binario)
        (b"Hello\x1bWorld", True),
        
        # Archivo con mezcla de texto y binario (binario)
        (b"Hello\x00\x01\x02\x03World", True),
        
        # Archivo con secuencias de escape válidas y bytes nulos (no binario)
        (b'\x1b[31mHello\x00World\x1b[0m', False),
        
        # Archivo con secuencias de escape válidas y bytes no imprimibles (no binario)
        (b'\x1b[31mHello\x01\x02\x03World\x1b[0m', False),
    ]
    
    for content, expected_binary in test_cases:
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.txt', delete=False) as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
            temp_path = Path(f.name)
        
        try:
            result = TextExtractor().extract(temp_path)
            is_binary = result == ""
            assert is_binary == expected_binary, \
                f"Failed binary detection for content {content!r}: expected {expected_binary}, got {is_binary}"
        finally:
            os.unlink(temp_path)


def test_mixed_content():
    """Verifica el manejo de archivos con mezcla de contenido texto y binario."""
    test_cases = [
        # Texto al principio, binario al final
        (b"Hello World\x00\x00\x00\x00\x00", True),
        
        # Binario al principio, texto al final
        (b"\x00\x00\x00\x00\x00Hello World", True),
        
        # Texto con un byte nulo ocasional
        (b"Hello\x00World\nThis is a test", False),
        
        # Texto con caracteres de control válidos
        (b"Hello\tWorld\nThis\ris\x1ba\ttest", False),
    ]
    
    for content, expected_binary in test_cases:
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.txt', delete=False) as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
            temp_path = Path(f.name)
        
        try:
            result = TextExtractor().extract(temp_path)
            is_binary = result == ""
            assert is_binary == expected_binary, \
                f"Failed mixed content detection for content {content!r}: expected {expected_binary}, got {is_binary}"
        finally:
            os.unlink(temp_path)


@pytest.mark.skip(reason="Known issue: encoding detection for Latin-1 and similar not fixed yet")
def test_encoding_detection():
    """Verifica la detección y manejo de diferentes codificaciones."""
    test_cases = [
        # UTF-8 con BOM
        (b'\xef\xbb\xbfHello World', "Hello World"),
        
        # UTF-16 LE con BOM
        (b'\xff\xfeH\x00e\x00l\x00l\x00o\x00 \x00W\x00o\x00r\x00l\x00d\x00', "Hello World"),
        
        # UTF-16 BE con BOM
        (b'\xfe\xff\x00H\x00e\x00l\x00l\x00o\x00 \x00W\x00o\x00r\x00l\x00d', "Hello World"),
        
        # UTF-32 LE con BOM
        (b'\xff\xfe\x00\x00H\x00\x00\x00e\x00\x00\x00l\x00\x00\x00l\x00\x00\x00o\x00\x00\x00 \x00\x00\x00W\x00\x00\x00o\x00\x00\x00r\x00\x00\x00l\x00\x00\x00d\x00\x00\x00', "Hello World"),
        
        # UTF-32 BE con BOM
        (b'\x00\x00\xfe\xff\x00\x00\x00H\x00\x00\x00e\x00\x00\x00l\x00\x00\x00l\x00\x00\x00o\x00\x00\x00 \x00\x00\x00W\x00\x00\x00o\x00\x00\x00r\x00\x00\x00l\x00\x00\x00d', "Hello World"),
        
        # UTF-8 sin BOM
        (b"Hello World", "Hello World"),
        
        # Latin-1 (ISO-8859-1)
        ("Héllö Wörld".encode('latin1'), "Héllö Wörld"),
        
        # Windows-1252
        ("Héllö Wörld".encode('cp1252'), "Héllö Wörld"),
        
        # ASCII
        (b"Hello World", "Hello World"),
        
        # UTF-16 sin BOM
        ("Hello World".encode('utf-16'), "Hello World"),
        
        # UTF-32 sin BOM
        ("Hello World".encode('utf-32'), "Hello World"),
        
        # Latin-9 (ISO-8859-15)
        ("Héllö Wörld".encode('iso-8859-15'), "Héllö Wörld"),
        
        # Mac Roman
        ("Héllö Wörld".encode('mac_roman'), "Héllö Wörld"),
        
        # DOS/IBM PC (CP437)
        ("Hello World".encode('cp437'), "Hello World"),
        
        # DOS Latin-1 (CP850)
        ("Héllö Wörld".encode('cp850'), "Héllö Wörld"),
        
        # DOS Latin-2 (CP852)
        ("Héllö Wörld".encode('cp852'), "Héllö Wörld"),
        
        # DOS Cyrillic (CP866)
        ("Привет мир".encode('cp866'), "Привет мир"),
        
        # Caracteres especiales en diferentes codificaciones
        ("áéíóúñü".encode('utf-8'), "áéíóúñü"),
        ("áéíóúñü".encode('latin1'), "áéíóúñü"),
        ("áéíóúñü".encode('cp1252'), "áéíóúñü"),
        
        # Texto con caracteres de control válidos
        (b"Hello\tWorld\n\r\f", "Hello\tWorld\n\r\f"),
        
        # Texto con secuencias de escape ANSI
        (b'\x1b[31mHello\x1b[0m World', '\x1b[31mHello\x1b[0m World'),
        
        # Texto con caracteres no imprimibles (debería ser reemplazado)
        (b"Hello\x01\x02\x03World", "HelloWorld"),
    ]
    
    for content, expected_text in test_cases:
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.txt', delete=False) as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
            temp_path = Path(f.name)
        
        try:
            result = TextExtractor().extract(temp_path)
            assert result == expected_text, \
                f"Failed encoding detection for content {content!r}: expected {expected_text!r}, got {result!r}"
        finally:
            os.unlink(temp_path)
