import os
import shutil

def eliminar_pycache(ruta_base="."):
    print(f"🔍 Buscando carpetas '__pycache__' en: {os.path.abspath(ruta_base)}\n")

    eliminadas = 0

    for root, dirs, files in os.walk(ruta_base):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                path_completo = os.path.join(root, dir_name)
                try:
                    shutil.rmtree(path_completo)
                    print(f"🧹 Eliminado: {path_completo}")
                    eliminadas += 1
                except Exception as e:
                    print(f"❌ Error eliminando {path_completo}: {e}")

    if eliminadas == 0:
        print("✅ No se encontraron carpetas '__pycache__'.")
    else:
        print(f"\n✅ Se eliminaron {eliminadas} carpetas '__pycache__'.")

if __name__ == "__main__":
    eliminar_pycache(".")  # Podés cambiar "app" por "." si querés limpiar todo el proyecto
