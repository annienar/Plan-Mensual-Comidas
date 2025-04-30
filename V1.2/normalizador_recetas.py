import re
import json

def normalizar_receta_desde_texto(texto):
    nombre = extraer_nombre(texto)
    calorias = extraer_calorias(texto)
    ingredientes = parsear_ingredientes(texto)
    preparacion = extraer_preparacion(texto)
    tags = inferir_tags(ingredientes, preparacion)

    return {
        "nombre": nombre,
        "calorias": calorias,
        "ingredientes": ingredientes,
        "preparacion": preparacion,
        "tags": tags
    }

def extraer_nombre(texto):
    lineas = texto.strip().splitlines()
    for linea in lineas:
        if linea.strip():  # salta líneas vacías
            return linea.strip()
    return "Receta sin nombre"

def extraer_calorias(texto):
    match = re.search(r"(?:[Cc]alor[ií]as|[Cc]alories)[:\s]+(\d+)", texto)
    return int(match.group(1)) if match else 0

def parsear_ingredientes(texto):
    patrones = ["ingredientes", "ingredients"]
    ingredientes = []
    for encabezado in patrones:
        match = re.search(rf"{encabezado}[:\n]", texto, re.IGNORECASE)
        if match:
            seccion = texto[match.end():]
            lineas = seccion.strip().splitlines()
            for linea in lineas:
                if not linea.strip() or any(p in linea.lower() for p in ["preparación", "instrucciones", "preparation", "instructions"]):
                    break
                ingrediente = parsear_linea_ingrediente(linea)
                if ingrediente:
                    ingredientes.append(ingrediente)
            break
    return ingredientes

def parsear_linea_ingrediente(linea):
    patron = r"(?P<cantidad>\d+(\.\d+)?)(\s+)?(?P<unidad>\w+)?\s+(?P<nombre>.+)"
    match = re.search(patron, linea.strip())
    if match:
        nombre = match.group("nombre").strip()
        if nombre.lower().startswith("de "):
            nombre = nombre[3:].strip()
        elif nombre.lower().startswith("of "):
            nombre = nombre[3:].strip()
        return {
            "nombre": nombre,
            "cantidad": float(match.group("cantidad")),
            "unidad": match.group("unidad") or "unidad"
        }
    return None


def extraer_preparacion(texto):
    posibles = ["preparación", "instrucciones", "preparation", "instructions"]
    for encabezado in posibles:
        match = re.search(rf"{encabezado}[:\n]", texto, re.IGNORECASE)
        if match:
            return texto[match.end():].strip()
    return ""

def inferir_tags(ingredientes, preparacion):
    tags = []
    if any("huevo" in i["nombre"].lower() or "egg" in i["nombre"].lower() for i in ingredientes):
        tags.append("proteico")
    if len(ingredientes) <= 4:
        tags.append("simple")
    return tags

# Prueba directa
if __name__ == "__main__":
    texto = """
    Avocado toast with egg
    Calories: 310

    Ingredients:
    - 2 slices of whole grain bread
    - 0.5 avocado
    - 1 egg

    Instructions:
    1. Toast the bread.
    2. Mash the avocado.
    3. Fry the egg and place on top.
    """

    receta = normalizar_receta_desde_texto(texto)
    print(json.dumps(receta, indent=2, ensure_ascii=False))
