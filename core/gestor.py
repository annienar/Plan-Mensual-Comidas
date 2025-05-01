"""
CLI principal para el Plan Mensual de Comidas.

Gestiona el procesamiento de recetas y generación de documentos.
"""

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List

from core.config import DIR_SIN_PROCESAR, NOMBRE_PROYECTO, VERSION
from core.generar_md import generar_md_todas
from core.logger import configurar_logger, log_error, log_info
from core.metadatos_recetas import normalizar_receta_desde_texto
from core.procesar_recetas import procesar_todo_en_sin_procesar

logger = configurar_logger("gestor")


class GestorRecetas:
    """Clase para gestionar el procesamiento y almacenamiento de recetas."""

    def procesar_receta(self, path: Path) -> Dict[str, Any]:
        """Procesa una receta desde un archivo.

        Args:
            path: Ruta al archivo de receta

        Returns:
            Dict con la receta normalizada
        """
        with open(path, "r", encoding="utf-8") as f:
            texto = f.read()
        return normalizar_receta_desde_texto(texto)

    def procesar_todas_recetas(self) -> List[Dict[str, Any]]:
        """Procesa todas las recetas en el directorio sin procesar.

        Returns:
            Lista de recetas normalizadas
        """
        recetas = []
        for path in DIR_SIN_PROCESAR.glob("*.txt"):
            recetas.append(self.procesar_receta(path))
        return recetas


def main() -> None:
    """Punto de entrada principal del CLI."""
    parser = argparse.ArgumentParser(
        prog=NOMBRE_PROYECTO.lower().replace(" ", "-"),
        description=f"{NOMBRE_PROYECTO} v{VERSION}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  %(prog)s --procesar                    # Procesa todos los archivos nuevos
  %(prog)s --generar-md                  # Genera Markdown de JSONs existentes
  %(prog)s --procesar --generar-md       # Flujo completo
  %(prog)s --test                        # Ejecuta las pruebas
  %(prog)s --version                     # Muestra la versión
        """,
    )

    parser.add_argument(
        "--procesar",
        action="store_true",
        help="Procesar todos los archivos en recetas/sin_procesar/",
    )
    parser.add_argument(
        "--generar-md",
        action="store_true",
        help="Generar archivos .md en recetas/procesadas/Recetas MD/",
    )
    parser.add_argument(
        "--test", action="store_true", help="Ejecutar la suite de tests con pytest"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
        help="Muestra la versión del programa",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="count",
        default=0,
        help="Aumenta el nivel de detalle en los mensajes",
    )

    args = parser.parse_args()

    # Si no se pasan flags, mostrar ayuda
    if not any([args.procesar, args.generar_md, args.test]):
        parser.print_help()
        sys.exit(0)

    exit_code = 0
    try:
        # Procesar archivos
        if args.procesar and not procesar_todo_en_sin_procesar():
            exit_code = 1

        # Generar Markdown
        if args.generar_md and not generar_md_todas():
            exit_code = 1

        # Ejecutar tests
        if args.test:
            import pytest

            test_args = ["-v"] if args.verbose else ["-q"]
            test_args.extend(["--maxfail=1"])
            exit_code = pytest.main(test_args)

    except KeyboardInterrupt:
        log_info("\n⚠️ Operación interrumpida por el usuario")
        exit_code = 130
    except Exception as e:
        log_error(f"❌ Error inesperado: {e}")
        exit_code = 1

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
