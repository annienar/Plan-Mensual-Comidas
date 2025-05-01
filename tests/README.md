# Tests del Sistema de Gestión de Recetas

Este directorio contiene los tests automatizados para el sistema de gestión de recetas. Los tests están organizados en tres categorías principales para mantener una clara separación de responsabilidades.

## Estructura de Directorios

```
tests/
├── unit/           # Tests unitarios
│   ├── test_extraer_txt.py    # Tests de extracción de texto
│   ├── test_extraer_pdf.py    # Tests de extracción de PDF
│   └── test_parser.py         # Tests del parser de recetas
├── integration/    # Tests de integración
│   ├── test_normalizador_recetas.py  # Tests de normalización
│   └── test_notion_sync.py           # Tests de sincronización con Notion
└── core/           # Tests de funcionalidad core
    ├── test_receta.py        # Tests de estructura de recetas
    ├── test_metadatos.py     # Tests de metadatos
    └── test_gestor.py        # Tests del gestor principal
```

## Tipos de Tests

### Tests Unitarios (`unit/`)
Tests que verifican componentes individuales del sistema:
- Extracción de texto de diferentes formatos
- Parsing de ingredientes y pasos
- Validación de formatos

### Tests de Integración (`integration/`)
Tests que verifican la interacción entre componentes:
- Proceso completo de normalización
- Sincronización con Notion
- Manejo de diferentes formatos de archivo

### Tests Core (`core/`)
Tests de funcionalidad central del sistema:
- Estructura de recetas
- Gestión de metadatos
- Operaciones del gestor

## Marcadores de Tests

Se utilizan los siguientes marcadores para categorizar los tests:

- `@pytest.mark.unit`: Tests unitarios
- `@pytest.mark.integration`: Tests de integración
- `@pytest.mark.notion`: Tests que requieren acceso a Notion
- `@pytest.mark.slow`: Tests que son particularmente lentos

## Configuración

### Variables de Entorno
Para ejecutar los tests que requieren Notion, necesitas configurar:

```bash
# .env o .env.test
NOTION_TOKEN=your_integration_token
NOTION_DATABASE_ID=your_database_id
```

### Pytest
La configuración de pytest está en `pytest.ini`:
- Descubrimiento automático de tests
- Reportes de cobertura
- Manejo de marcadores
- Configuración de entorno

## Ejecución de Tests

### Todos los Tests
```bash
pytest
```

### Tests por Categoría
```bash
# Tests unitarios
pytest tests/unit/

# Tests de integración
pytest tests/integration/

# Tests core
pytest tests/core/
```

### Tests por Marcador
```bash
# Solo tests unitarios
pytest -m unit

# Tests que no requieren Notion
pytest -m "not notion"

# Tests de integración que no son lentos
pytest -m "integration and not slow"
```

### Cobertura de Tests
```bash
# Generar reporte de cobertura
pytest --cov=core --cov-report=html
```

## Buenas Prácticas

1. **Nombrado de Tests**
   - Usar nombres descriptivos que indiquen qué se está probando
   - Seguir el patrón `test_<funcionalidad>_<escenario>`

2. **Fixtures**
   - Usar fixtures para código común
   - Mantener fixtures lo más simples posible
   - Documentar el propósito de cada fixture

3. **Assertions**
   - Usar mensajes descriptivos en assertions
   - Verificar tanto casos positivos como negativos
   - Incluir validación de tipos y rangos

4. **Organización**
   - Un archivo de test por módulo
   - Mantener tests relacionados juntos
   - Separar claramente diferentes tipos de tests

5. **Documentación**
   - Documentar el propósito de cada test
   - Incluir ejemplos de uso cuando sea relevante
   - Mantener actualizada la documentación

## Mantenimiento

### Añadir Nuevos Tests
1. Identificar la categoría apropiada (unit/integration/core)
2. Crear el archivo de test siguiendo las convenciones de nombrado
3. Añadir los marcadores apropiados
4. Documentar el propósito y requisitos

### Actualizar Tests Existentes
1. Mantener la compatibilidad con tests existentes
2. Actualizar la documentación según sea necesario
3. Verificar que no se rompen otros tests

## Troubleshooting

### Problemas Comunes

1. **Tests de Notion Fallan**
   - Verificar credenciales en .env
   - Confirmar acceso a la API
   - Verificar permisos de la base de datos

2. **Tests Lentos**
   - Usar el marcador @pytest.mark.slow
   - Considerar mocking para tests que no requieren API real

3. **Conflictos de Dependencias**
   - Verificar requirements.txt
   - Usar entorno virtual limpio
   - Actualizar dependencias si es necesario
