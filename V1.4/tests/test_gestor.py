import os
import hashlib
import json
from dotenv import load_dotenv
from notion_client import Client


from core.logger import configurar_logger, log_info, log_warning, log_error
from core.notificaciones import log_receta_normalizada

logger = configurar_logger("gestor")

# ------------------------------------------------------------------
# GestorPlanComidas
# ------------------------------------------------------------------
# Encargado de comunicar las recetas normalizadas a Notion.
# (Versión limpia: sin bloques de prueba / demo.)
# ------------------------------------------------------------------

class GestorPlanComidas:
    def __init__(self):
        load_dotenv()
        self.notion = Client(auth=os.environ.get("NOTION_TOKEN"))
        self.db_recetas        = os.environ.get("NOTION_RECETAS_DB")
        self.db_alacena        = os.environ.get("NOTION_ALACENA_DB")
        self.db_ingredientes   = os.environ.get("NOTION_INGREDIENTES_DB")
        self.db_lista_compras  = os.environ.get("NOTION_LISTA_COMPRAS_DB")

    # --------------------------------------------------------------
    # Helpers
    # --------------------------------------------------------------
    @staticmethod
    def _hash_receta(receta: dict) -> str:
        """Hash estable para detectar cambios en la receta."""
        contenido = {
            "nombre": receta["nombre"],
            "calorias": receta.get("calorias", 0),
            "preparacion": receta.get("preparacion", ""),
            "ingredientes": sorted(
                f"{i['nombre']}:{i.get('cantidad', 0)}:{i.get('unidad', '')}"
                for i in receta.get("ingredientes", [])
            ),
        }
        return hashlib.md5(json.dumps(contenido, sort_keys=True).encode()).hexdigest()

    # --------------------------------------------------------------
    # Búsqueda y CRUD en Notion
    # --------------------------------------------------------------
    def _buscar_por_nombre(self, nombre: str):
        try:
            resp = self.notion.databases.query(
                database_id=self.db_recetas,
                filter={
                    "property": "Nombre",
                    "title": {"equals": nombre},
                },
            )
            return resp["results"][0] if resp["results"] else None
        except Exception as e:
            log_error(f"Error al buscar receta en Notion: {e}")
            return None

    def _crear_receta(self, receta: dict) -> bool:
        try:
            self.notion.pages.create(
                parent={"database_id": self.db_recetas},
                properties={
                    "Nombre": {"title": [{"text": {"content": receta["nombre"]}}]},
                    "Calorías": {"number": receta.get("calorias", 0)},
                    "Preparación": {"rich_text": [{"text": {"content": receta.get("preparacion", "")}}]},
                    "Tags": {"multi_select": [{"name": t} for t in receta.get("tags", [])]},
                },
            )
            log_info(f"🆕 Receta creada: {receta['nombre']}")
            return True
        except Exception as e:
            log_error(f"Error al crear receta: {e}")
            return False

    def _actualizar_receta(self, page_id: str, receta: dict) -> bool:
        try:
            self.notion.pages.update(
                page_id=page_id,
                properties={
                    "Nombre": {"title": [{"text": {"content": receta["nombre"]}}]},
                    "Calorías": {"number": receta.get("calorias", 0)},
                    "Preparación": {"rich_text": [{"text": {"content": receta.get("preparacion", "")}}]},
                    "Tags": {"multi_select": [{"name": t} for t in receta.get("tags", [])]},
                },
            )
            log_info(f"🔄 Receta actualizada: {receta['nombre']}")
            return True
        except Exception as e:
            log_error(f"Error al actualizar receta: {e}")
            return False

    # --------------------------------------------------------------
    # API pública
    # --------------------------------------------------------------
    def subir_recetas(self, recetas: list[dict]):
        """Recibe lista de dict (normalizados) y los sincroniza con Notion."""
        stats = {"creadas": 0, "actualizadas": 0, "omitidas": 0}

        for r in recetas:
            log_info(f"📌 Procesando receta: {r['nombre']}")
            log_receta_normalizada(r["nombre"])
            existente = self._buscar_por_nombre(r["nombre"])

            if existente:
                mismo_contenido = self._hash_receta(r) == self._hash_receta(
                    self._extraer_r_local(existente)
                )
                if mismo_contenido:
                    log_warning("⏩ Receta idéntica; omitida")
                    stats["omitidas"] += 1
                    continue
                if self._actualizar_receta(existente["id"], r):
                    stats["actualizadas"] += 1
                else:
                    stats["omitidas"] += 1
            else:
                if self._crear_receta(r):
                    stats["creadas"] += 1
                else:
                    stats["omitidas"] += 1

        log_info(
            f"🏁 Resumen → Creadas: {stats['creadas']} • Actualizadas: {stats['actualizadas']} • Omitidas: {stats['omitidas']}"
        )
        return stats

    # --------------------------------------------------------------
    # Util para comparar cambios — extrae receta existente a dict
    # --------------------------------------------------------------
    def _extraer_r_local(self, page_json):
        props = page_json["properties"]
        nombre = props.get("Nombre", {}).get("title", [{}])[0].get("plain_text", "")
        calorias = props.get("Calorías", {}).get("number", 0)
        preparacion = props.get("Preparación", {}).get("rich_text", [{}])[0].get("plain_text", "")
        tags = [t["name"] for t in props.get("Tags", {}).get("multi_select", [])]
        # Ingredientes se omiten aquí; asumirás lógica separada.
        return {
            "nombre": nombre,
            "calorias": calorias,
            "preparacion": preparacion,
            "ingredientes": [],
            "tags": tags,
        }
