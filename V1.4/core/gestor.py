import argparse
import sys

from core.procesar_recetas import procesar_todo_en_sin_procesar
from core.generar_md import generar_md_todas


def main():
    parser = argparse.ArgumentParser(
        prog="plan-menusal",
        description="CLI para el Plan Mensual de Comidas v1.4.9"
    )

    parser.add_argument(
        "--procesar",
        action="store_true",
        help="Procesar todos los archivos en recetas/sin_procesar/"
    )
    parser.add_argument(
        "--generar-md",
        action="store_true",
        help="Generar archivos .md en recetas/procesadas/Recetas MD/"
    )
    parser.add_argument(
        "--tests",
        action="store_true",
        help="Ejecutar la suite de tests con pytest"
    )

    args = parser.parse_args()

    # Si no se pasan flags, ejecutar flujo completo
    if not (args.procesar or args.generar_md or args.tests):
        args.procesar = True
        args.generar_md = True

    # Ejecutar acciones según flags
    if args.procesar:
        procesar_todo_en_sin_procesar()
    if args.generar_md:
        generar_md_todas()
    if args.tests:
        # Llama a pytest
        sys.exit(__import__("pytest").main(["-q", "--maxfail=1"]))

if __name__ == "__main__":
    main()
