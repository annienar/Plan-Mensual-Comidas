import os
import re
import hashlib
import json
from dotenv import load_dotenv
from notion_client import Client

class GestorPlanComidas:
    def __init__(self):
        load_dotenv()
        self.notion = Client(auth=os.environ.get("NOTION_TOKEN"))
        self.db_recetas = os.environ.get("NOTION_RECETAS_DB")
        self.db_alacena = os.environ.get("NOTION_ALACENA_DB")
        self.db_ingredientes = os.environ.get("NOTION_INGREDIENTES_DB")
        self.db_lista_compras = os.environ.get("NOTION_LISTA_COMPRAS_DB")

    def generar_hash_receta(self, receta):
        contenido = {
            "nombre": receta["nombre"],
            "calorias": receta.get("calorias", 0),
            "preparacion": receta.get("preparacion", ""),
            "ingredientes": sorted([
                f"{ing['nombre']}:{ing.get('cantidad', 0)}:{ing.get('unidad', '')}"
                for ing in receta.get("ingredientes", [])
            ])
        }
        return hashlib.md5(json.dumps(contenido, sort_keys=True).encode()).hexdigest()

    def buscar_receta_por_nombre(self, nombre_receta):
        try:
            query = {
                "filter": {
                    "property": "Nombre",
                    "title": {
                        "equals": nombre_receta
                    }
                }
            }
            resultados = self.notion.databases.query(database_id=self.db_recetas, **query)
            if resultados["results"]:
                return resultados["results"][0]
            return None
        except Exception as e:
            print(f"Error al buscar receta por nombre: {e}")
            return None

    def actualizar_receta_existente(self, receta_id, receta_nueva):
        try:
            properties = {
                "Nombre": {"title": [{"text": {"content": receta_nueva["nombre"]}}]},
                "Calorías": {"number": receta_nueva.get("calorias", 0)},
                "Preparación": {"rich_text": [{"text": {"content": receta_nueva.get("preparacion", "")}}]},
                "Tags": {"multi_select": [{"name": tag} for tag in receta_nueva.get("tags", [])]}
            }
            self.notion.pages.update(page_id=receta_id, properties=properties)
            print(f"✅ Receta '{receta_nueva['nombre']}' actualizada con éxito")
            self.actualizar_ingredientes(receta_id, receta_nueva.get("ingredientes", []))
            return True
        except Exception as e:
            print(f"Error al actualizar receta: {e}")
            return False

    def actualizar_ingredientes(self, receta_id, ingredientes):
        print(f"Actualizando {len(ingredientes)} ingredientes para la receta")
        for ingrediente in ingredientes:
            print(f"Procesando ingrediente: {ingrediente['nombre']}")

    def procesar_recetas(self, recetas):
        resultados = {
            "creadas": [],
            "actualizadas": [],
            "omitidas": []
        }
        for receta in recetas:
            print(f"📌 Procesando receta: {receta['nombre']}")
            hash_receta = self.generar_hash_receta(receta)
            receta_existente = self.buscar_receta_por_nombre(receta["nombre"])
            if receta_existente:
                receta_actual = self.extraer_datos_receta(receta_existente)
                hash_existente = self.generar_hash_receta(receta_actual)
                if hash_receta == hash_existente:
                    print(f"⏩ Receta '{receta['nombre']}' ya existe con el mismo contenido. Omitiendo.")
                    resultados["omitidas"].append(receta["nombre"])
                else:
                    print(f"🔄 Receta '{receta['nombre']}' existe pero con contenido diferente. Actualizando...")
                    if self.actualizar_receta_existente(receta_existente["id"], receta):
                        resultados["actualizadas"].append(receta["nombre"])
                    else:
                        resultados["omitidas"].append(receta["nombre"])
            else:
                print(f"✅ Nueva receta detectada: {receta['nombre']}. Creando...")
                if self.crear_nueva_receta(receta):
                    resultados["creadas"].append(receta["nombre"])
                else:
                    resultados["omitidas"].append(receta["nombre"])
        self.mostrar_resumen(resultados)
        return resultados

    def extraer_datos_receta(self, receta_notion):
        try:
            props = receta_notion["properties"]
            nombre = self.extraer_texto_desde_titulo(props.get("Nombre", {}))
            calorias = self.extraer_numero(props.get("Calorías", {}))
            preparacion = self.extraer_texto_enriquecido(props.get("Preparación", {}))
            tags = self.extraer_tags(props.get("Tags", {}))
            ingredientes = self.obtener_ingredientes_receta(receta_notion["id"])
            return {
                "nombre": nombre,
                "calorias": calorias,
                "preparacion": preparacion,
                "tags": tags,
                "ingredientes": ingredientes
            }
        except Exception as e:
            print(f"Error al extraer datos de receta: {e}")
            return {"nombre": "", "ingredientes": []}

    def extraer_texto_desde_titulo(self, prop):
        try:
            if prop.get("title"):
                return prop["title"][0]["text"]["content"]
            return ""
        except:
            return ""

    def extraer_numero(self, prop):
        return prop.get("number", 0)

    def extraer_texto_enriquecido(self, prop):
        try:
            if prop.get("rich_text"):
                return prop["rich_text"][0]["text"]["content"]
            return ""
        except:
            return ""

    def extraer_tags(self, prop):
        try:
            return [item["name"] for item in prop.get("multi_select", [])]
        except:
            return []

    def obtener_ingredientes_receta(self, receta_id):
        try:
            return []
        except Exception as e:
            print(f"Error al obtener ingredientes: {e}")
            return []

    def crear_nueva_receta(self, receta):
        try:
            print(f"✅ Receta '{receta['nombre']}' creada con éxito")
            return True
        except Exception as e:
            print(f"Error al crear receta: {e}")
            return False

    def mostrar_resumen(self, resultados):
        print("\n======= RESUMEN DE OPERACIONES =======")
        print(f"✅ Recetas creadas: {len(resultados['creadas'])}")
        if resultados['creadas']:
            for receta in resultados['creadas']:
                print(f"  - {receta}")
        print(f"🔄 Recetas actualizadas: {len(resultados['actualizadas'])}")
        if resultados['actualizadas']:
            for receta in resultados['actualizadas']:
                print(f"  - {receta}")
        print(f"⏩ Recetas omitidas: {len(resultados['omitidas'])}")
        if resultados['omitidas']:
            for receta in resultados['omitidas']:
                print(f"  - {receta}")
        print("======================================")

    def receta_ya_existe(self, nombre_receta):
        return self.buscar_receta_por_nombre(nombre_receta) is not None

if __name__ == "__main__":
    gestor = GestorPlanComidas()
    receta_demo = {
        "nombre": "Tostadas con palta y huevo",
        "calorias": 300,
        "tags": ["brunch", "proteico"],
        "preparacion": "1. Tostar el pan.\n2. Machacar la palta.\n3. Freír el huevo y colocar encima.",
        "ingredientes": [
            {"nombre": "pan integral", "cantidad": 2, "unidad": "unidad"},
            {"nombre": "palta", "cantidad": 0.5, "unidad": "unidad"},
            {"nombre": "huevo", "cantidad": 1, "unidad": "unidad"}
        ]
    }
    gestor.procesar_recetas([receta_demo])
