import os
from zipfile import ZipFile
from datetime import datetime

ZIP_FOLDER = "ZIP"
VERSION_FILE = "VERSION.txt"
CHANGELOG_FILE = "changelog.txt"
NOTION_FILE = "notion_v1_4.md"
SUMMARY_FILE = "resumen.txt"

def cargar_version_actual():
    if not os.path.exists(VERSION_FILE):
        return (1, 4, 0)
    with open(VERSION_FILE, "r") as f:
        partes = f.read().strip().split(".")
        return tuple(map(int, partes))

def incrementar_version(version):
    major, minor, patch = version
    return (major, minor, patch + 1)

def guardar_version(version):
    with open(VERSION_FILE, "w") as f:
        f.write(".".join(map(str, version)))

def agregar_a_changelog(version, timestamp, resumen):
    with open(CHANGELOG_FILE, "a") as f:
        f.write(f"Versión: {version}\n")
        f.write(f"Fecha: {timestamp}\n")
        f.write(f"{resumen}\n---\n\n")

def agregar_a_notion(version, timestamp, resumen):
    with open(NOTION_FILE, "a") as f:
        f.write(f"# 🧾 Plan Mensual Comidas – Versión {version}\n")
        f.write(f"## 🕒 Fecha\n{timestamp}\n\n")
        f.write(resumen)
        f.write("\n---\n\n")

def generar_zip(version):
    os.makedirs(ZIP_FOLDER, exist_ok=True)
    nombre_zip = f"plan_mensual_comidas_v{'_'.join(map(str, version))}.zip"
    zip_path = os.path.join(ZIP_FOLDER, nombre_zip)

    with ZipFile(zip_path, "w") as zipf:
        for carpeta in ["core", "tests", "recetas"]:
            for root, _, files in os.walk(carpeta):
                for file in files:
                    path = os.path.join(root, file)
                    zipf.write(path, arcname=path)
        for archivo in ["VERSION.txt", "changelog.txt", "notion_v1_4.md", ".env"]:
            if os.path.exists(archivo):
                zipf.write(archivo)

    print(f"✅ ZIP generado en carpeta {ZIP_FOLDER}/: {zip_path}")

def main():
    actual = cargar_version_actual()
    nueva = incrementar_version(actual)
    guardar_version(nueva)

    if not os.path.exists(SUMMARY_FILE):
        print(f"❌ Falta el archivo {SUMMARY_FILE} con el resumen técnico.")
        return

    with open(SUMMARY_FILE, "r") as f:
        resumen_tecnico = f.read()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    version_str = ".".join(map(str, nueva))

    agregar_a_changelog(version_str, timestamp, resumen_tecnico)
    agregar_a_notion(version_str, timestamp, resumen_tecnico)
    generar_zip(nueva)

if __name__ == "__main__":
    main()
