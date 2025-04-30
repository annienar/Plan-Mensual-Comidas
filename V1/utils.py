
import re
from difflib import SequenceMatcher

def normalizar_texto(texto):
    return texto.lower().strip()

def encontrar_duplicado(nombre, lista_existente):
    nombre_normalizado = normalizar_texto(nombre)
    for item in lista_existente:
        existente = normalizar_texto(item["Name"]["title"][0]["text"]["content"])
        if SequenceMatcher(None, nombre_normalizado, existente).ratio() > 0.9:
            return item["id"]
    return None

def obtener_categoria_desde_nombre(nombre):
    categorias = {
        "fruta": ["banana", "manzana", "palta"],
        "lacteo": ["leche", "queso", "yogur"],
        "panificados": ["tostada", "pan", "waffle"],
        "proteína": ["huevo", "jamón"],
        "semillas y frutos secos": ["chía", "cajú", "almendra"],
    }
    nombre = normalizar_texto(nombre)
    for categoria, palabras in categorias.items():
        if any(palabra in nombre for palabra in palabras):
            return categoria
    return "sin categoría"

def obtener_unidad_desde_nombre(nombre):
    unidades = {
        "g": ["harina", "azúcar", "avena", "polvo", "cacao", "manteca", "queso", "chía", "cajú", "almendra"],
        "ml": ["leche", "agua", "vinagre", "aceite"],
        "unidad": ["banana", "huevo", "pan", "tostada", "tomate", "waffle"]
    }
    nombre = normalizar_texto(nombre)
    for unidad, palabras in unidades.items():
        if any(palabra in nombre for palabra in palabras):
            return unidad
    return "unidad"
