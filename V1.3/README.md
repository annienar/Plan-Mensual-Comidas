# 🥗 Plan Mensual de Comidas – Versión 1.3

## ✅ Estructura del Proyecto

```
plan_mensual_comidas/
├── core/
│   ├── gestor.py
│   ├── normalizador_recetas.py
│   └── procesar_recetas.py
│
├── tests/
│   ├── test_gestor.py
│   ├── test_normalizador_recetas.py
│   └── test_procesar_recetas.py
│
├── recetas/
│   ├── sin_procesar/
│   └── procesadas/
│       ├── Receta Original/
│       └── Recetas JSON/
│
├── .log/
├── .env.template
└── requirements.txt
```

## 📄 Tabla de Scripts

| Archivo                          | Rol                                                             |
|----------------------------------|------------------------------------------------------------------|
| `gestor.py`                      | Lógica principal de integración con Notion                      |
| `normalizador_recetas.py`       | Parser que convierte texto en receta estructurada               |
| `procesar_recetas.py`           | Procesa recetas desde carpeta `sin_procesar/` a JSON + backup   |
| `test_gestor.py`                | Simula procesamiento con Notion: crea JSON y mueve original     |
| `test_normalizador_recetas.py`  | Prueba del parser individual                                     |
| `test_procesar_recetas.py`      | Test de procesamiento por lote de recetas sin subir a Notion    |

## 📂 Carpeta `recetas/`

Organización para control de flujo:

- `sin_procesar/`: recetas pendientes en `.txt`
- `procesadas/Receta Original/`: .txt original ya procesado
- `procesadas/Recetas JSON/`: resultado parseado (`.json`)

## 🛠️ Estado del Proyecto

- ✅ Parser funcional para español e inglés
- ✅ Procesamiento por lote
- ✅ Simulación sin conexión a Notion
- ✅ Logs individuales por ejecución
- ⚠️ Próxima versión (1.4): OCR para JPG/PDF y logs de consola reflejados en archivo


## 🪵 Sistema de Logs

Todos los scripts (`core/` y `tests/`) utilizan un sistema de logging modular importado desde `core/logger.py`.

Cada ejecución genera un archivo `.log` único con el siguiente formato:

```
.log/
└── log-MM-DD-HHMM-nombrescript.txt
```

Por ejemplo:

```
log-06-10-1545-test_gestor.txt
log-06-10-1546-gestor.txt
```

### Uso en cualquier archivo

```python
from core.logger import configurar_logger
logger = configurar_logger("nombre_del_script")

print("mensaje visible")
logger.info("mensaje registrado")
```

Los mensajes `print()` se mantienen para visualización directa, pero todo queda trazado en archivo también.

