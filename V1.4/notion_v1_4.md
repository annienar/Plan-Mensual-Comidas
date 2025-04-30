# 🧾 Plan Mensual Comidas – Versión 1.4.1
## 🕒 Fecha
2025-04-24 10:58:37

- Actualización automática.
- Cambios técnicos y refactor del logger.
- Manejo de campo origen con detección y ausencia.
---

# 🧾 Plan Mensual Comidas – Versión 1.4.2
## 🕒 Fecha
2025-04-24 11:01:54

- Actualización automática.
- Cambios técnicos y refactor del logger.
- Manejo de campo origen con detección y ausencia.
---

# 🧾 Plan Mensual Comidas – Versión 1.4.3
## 🕒 Fecha
2025-04-24 11:08:27

- Actualización automática.
- Cambios técnicos y refactor del logger.
- Manejo de campo origen con detección y ausencia.
---

# 🧾 Plan Mensual Comidas – Versión 1.4.4
## 🕒 Fecha
2025-04-24 14:17:54

- Centralización de toda la lógica de impresión y logging en `core/logger.py`.
- Se reemplazó el uso directo de `print()` y `logger.*` por funciones como `log_info`, `log_error`, `log_archivo_movido`, etc.
- Se añadieron funciones específicas para registrar eventos: creación de carpetas, movimiento de archivos, generación de JSONs, y normalización de recetas.
- Se eliminó la impresión del JSON en consola y logs.
- Se agregó detección y registro explícito de la presencia o ausencia del campo `origen` (URL).
---

# 🧾 Plan Mensual Comidas – Versión 1.4.5
## 🕒 Fecha
2025-04-24 14:29:42

- Se eliminó el hardcode del resumen técnico en el script `zip_proyecto.py`.
- El resumen técnico ahora se lee desde un archivo externo `resumen.txt`, que debe mantenerse actualizado antes de cada empaquetado.
- Esto permite mayor flexibilidad y separación de responsabilidades entre automatización y documentación técnica.
- El archivo `zip_proyecto.py` genera automáticamente:
  - Un `.zip` con la estructura del proyecto en la carpeta `ZIP/`
  - Un `VERSION.txt` con la versión actual
  - Una entrada en `changelog.txt`
  - Una entrada en `notion_v1_4.md` con el mismo resumen
- Se conserva la lógica de versionado incremental (1.4.X).
- Se mantiene el registro completo de logs estructurado por consola y archivo (`.log/`) incluyendo la ausencia de URL (`log_sin_origen_detectado()`).


---

# 🧾 Plan Mensual Comidas – Versión 1.4.6
## 🕒 Fecha
2025-04-24 17:47:01

- Se validó exitosamente el procesamiento de un PDF complejo con título largo y fuente de blog.
- Se confirmó el registro correcto del campo `origen` al detectar una URL dentro del contenido.
- Se detectó un problema en la extracción del nombre: la URL fue incluida dentro del campo `nombre`, lo que será corregido en la próxima iteración.
- Se identificó que el sistema no logró extraer los ingredientes por posibles variaciones en el encabezado o formato libre de blog.
- Próxima mejora: mejorar `normalizador_recetas.py` para separar `origen` del `nombre` y mejorar la heurística de detección de ingredientes.

---

# 🧾 Plan Mensual Comidas – Versión 1.4.7
## 🕒 Fecha
2025-04-24 19:10:18

Cambios técnicos en la versión 1.4.6

    Se refactorizó extraer_nombre() para eliminar frases redundantes como “cómo hacerlo en casa paso a paso”, “receta fácil”, etc., y dejar solo el nombre limpio de la receta.

    Se agregó la función limpiar_nombre() para filtrar caracteres no deseados y mejorar el formateo del nombre.

    Se implementó la capitalización inteligente del nombre (capitalize() tras limpieza).

    Se corrigió el uso incorrecto del patrón r"https?://\\S+" en extraer_url_origen(), cambiándolo a r"https?://\S+" para detectar URLs reales.

    Se restauró la función extraer_url_origen() que había sido accidentalmente removida.

    Se incluyó el campo "origen" de forma obligatoria en el objeto receta, asignando "Desconocido" si no se detecta una URL.

    Se agregó una verificación para que la función extraer_url_origen() aparezca antes de ser usada dentro de normalizar_receta_desde_texto().

    Se mejoró la integración de funciones auxiliares (extraer_nombre, extraer_calorias, etc.) garantizando que estén definidas correctamente.

    Se confirmó el correcto funcionamiento de la normalización con múltiples tests usando test_procesar_recetas.py, incluyendo:

        Eliminación correcta de URL del campo "nombre"

        Inclusión de la URL en el campo "origen"

        Mantenimiento del nombre limpio

    Se estableció que futuras versiones trabajarán sobre la detección avanzada de ingredientes (v1.4.7).

---

# 🧾 Plan Mensual Comidas – Versión 1.4.8
## 🕒 Fecha
2025-04-27 18:08:02

# --------------------------------------------------------------------
#  Plan Mensual de Comidas – Resumen técnico
#  Estado de la versión 1.4.7  (cerrada el 27-abr-2025 17:15 ART)
# --------------------------------------------------------------------

Estructura de carpetas
──────────────────────
plan_mensual_comidas/
├─ core/                    ← lógica de negocio
│  ├─ __init__.py
│  ├─ extraer_txt.py
│  ├─ extraer_pdf.py
│  ├─ extraer_ocr.py
│  ├─ normalizador_recetas.py
│  ├─ procesar_recetas.py
│  ├─ logger.py             ← refactor v1.4.7
│  └─ gestor.py             ← aún v1.2 (contiene demo)
├─ tests/                   ← ejecución local, sin Notion
│  ├─ test_extraer_txt.py
│  ├─ test_extraer_pdf.py
│  └─ test_procesar_recetas.py
├─ recetas/
│  ├─ sin_procesar/         ← archivos de entrada (.txt/.pdf/.jpg)
│  └─ procesadas/
│     ├─ Receta Original/
│     └─ Recetas JSON/
├─ .log/
│  └─ 1.4.7/                ← 1 archivo por módulo con timestamp
├─ VERSION.txt              ← “1.4.7”
└─ requirements.txt         ← pdfplumber, pytesseract, python-dotenv, notion-client …

Logger (v1.4.7)
───────────────
✓ Un único root-logger.
✓ Console-handler sin duplicados.
✓ File-handler en “.log/1.4.7/log-…-<módulo>.txt”.
✓ Encabezado con versión SOLO en archivo.
✓ Warnings de pdfminer silenciados.

Extracción de texto
───────────────────
• extraer_txt.py        – OK (utf-8)
• extraer_pdf.py        – OK (pdfplumber; warnings silenciados)
• extraer_ocr.py        – OK (pdf → images → pytesseract)

Normalizador
────────────
• Detecta URL → campo “origen” (o “Desconocido”).
• Limpia títulos “cómo hacerlo… paso a paso”.
• Ingredientes simples             – funciona.
• Porciones / fracciones           – **pendiente** (para 1.4.8).
• Tags básicos (“proteico”, “simple”).

Procesador de recetas
─────────────────────
1. Detecta tipo de archivo → llama extractor.
2. Normaliza → mueve original → guarda JSON.
3. Rollback si falla guardado JSON.
4. Devuelve True/False por archivo procesado.
5. Resumen final (✅/❌) en consola y log.

Tests locales
─────────────
• test_extraer_txt.py   – lee cualquier .txt en *sin_procesar*.
• test_extraer_pdf.py   – idem para .pdf.
• test_procesar_recetas – procesa lote completo y muestra resumen.

Gestor Notion
─────────────
Estado: v1.2 demo con receta hard-codeada.
Falta: integrar logger y llamadas reales a Notion.

Pendiente para v1.4.8
─────────────────────
1. **Refactor gestor.py**  
   – Eliminar bloque demo.  
   – Usar wrappers de logger.  
   – Preparar tests test_gestor.py (sin acceder a Notion).

2. **Parseo avanzado de ingredientes**  
   – Unidades compuestas (g, ml, “1 ½ taza”).  
   – Detección de número de porciones (“para 9 panes”).

3. **Documentación / README**  
   – Pasos para crear venv, instalar reqs y ejecutar tests.

4. **Mejora de tests**  
   – PyTest + fixtures para varios ejemplos (txt & pdf).

# --------------------------------------------------------------------
# Fin de resumen – listo para archivar como 1.4.7 y abrir rama 1.4.8
# --------------------------------------------------------------------


---

