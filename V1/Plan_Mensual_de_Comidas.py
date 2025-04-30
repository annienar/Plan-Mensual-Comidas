# Plan_Mensual_de_Comidas.py - con mejoras
import os
import re
from dotenv import load_dotenv
from notion_client import Client
import logging
from datetime import datetime

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("plan_comidas.log"), logging.StreamHandler()]
)
logger = logging.getLogger("plan_comidas")

class GestorPlanComidas:
    def __init__(self):
        load_dotenv()
        self.notion = Client(auth=os.environ.get("NOTION_TOKEN"))
        self.db_recetas = os.environ.get("NOTION_RECETAS_DB")
        self.db_alacena = os.environ.get("NOTION_ALACENA_DB")
        self.db_ingredientes = os.environ.get("NOTION_INGREDIENTES_DB")
        self.db_lista_compras = os.environ.get("NOTION_LISTA_COMPRAS_DB")

    def procesar_recetas(self, recetas):
        for receta in recetas:
            logger.info(f"📌 Procesando receta: {receta['nombre']}")
            if self.receta_ya_existe(receta["nombre"]):
                logger.warning(f"⚠️ Receta '{receta['nombre']}' ya existe. Revisá si hay que actualizar.")
                continue
            logger.info(f"✅ Nueva receta detectada: {receta['nombre']}")

    def receta_ya_existe(self, nombre_receta):
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
            return bool(resultados["results"])
        except Exception as e:
            logger.error(f"Error al verificar existencia de receta: {e}")
            return False

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