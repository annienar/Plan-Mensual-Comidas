# crear_recetas.py - versión mejorada
import json
import sys
import argparse
from Plan_Mensual_de_Comidas import GestorPlanComidas

def procesar_receta_directa(datos_receta):
    """Procesa una receta proporcionada como diccionario"""
    gestor = GestorPlanComidas()
    if gestor.receta_ya_existe(datos_receta["nombre"]):
        print(f"⚠️ La receta '{datos_receta['nombre']}' ya existe en Notion.")
        confirmar = input("¿Querés crearla de todas formas? (s/n): ")
        if confirmar.lower() != 's':
            print("⛔ Operación cancelada.")
            return False
    gestor.procesar_recetas([datos_receta])
    print(f"✅ Receta '{datos_receta['nombre']}' procesada y enviada a Notion")
    return True

def crear_receta_interactiva():
    print("
===== CREACIÓN DE NUEVA RECETA =====")
    receta = {}

    receta["nombre"] = input("Nombre de la receta: ")
    try:
        receta["calorias"] = float(input("Calorías (por porción): "))
    except ValueError:
        receta["calorias"] = 0

    tags_input = input("Tags (separados por coma): ")
    receta["tags"] = [tag.strip() for tag in tags_input.split(",") if tag.strip()]

    print("Pasos de preparación (escribe 'fin' en una línea nueva para terminar):")
    pasos_prep = []
    while True:
        paso = input("> ")
        if paso.lower() == "fin":
            break
        pasos_prep.append(paso)
    receta["preparacion"] = "\n".join(pasos_prep)

    receta["ingredientes"] = []
    print("\nIngredientes (escribe 'fin' cuando termines):")
    while True:
        nombre_ingrediente = input("Nombre del ingrediente (o 'fin'): ")
        if nombre_ingrediente.lower() == "fin":
            break
        try:
            cantidad = float(input("Cantidad: "))
        except ValueError:
            cantidad = 1
        unidad = input("Unidad (g, ml, unidad, etc.): ")
        receta["ingredientes"].append({
            "nombre": nombre_ingrediente,
            "cantidad": cantidad,
            "unidad": unidad
        })

    return receta

def main():
    parser = argparse.ArgumentParser(description="Crear y procesar recetas")
    parser.add_argument('--interactivo', action='store_true', help='Crear receta de forma interactiva')
    parser.add_argument('--archivo', type=str, help='Ruta a archivo JSON con receta')
    args = parser.parse_args()

    if args.interactivo:
        receta = crear_receta_interactiva()
        confirmar = input("¿Procesar esta receta y enviarla a Notion? (s/n): ")
        if confirmar.lower() == "s":
            procesar_receta_directa(receta)

    elif args.archivo:
        try:
            with open(args.archivo, 'r', encoding='utf-8') as f:
                receta = json.load(f)
            procesar_receta_directa(receta)
        except Exception as e:
            print(f"❌ Error al leer el archivo: {e}")

if __name__ == "__main__":
    main()