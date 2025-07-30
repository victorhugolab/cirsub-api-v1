import subprocess
import sys

def install_package(package_name):
    print(f"📦 Instalando: {package_name}...")
    result = subprocess.run([sys.executable, "-m", "pip", "install", package_name])
    if result.returncode == 0:
        print("✅ Instalación exitosa.")
        print("📄 Actualizando requirements.txt...")
        subprocess.run([sys.executable, "-m", "pip", "freeze"], stdout=open("requirements.txt", "w"))
        print("📦 requirements.txt actualizado.")
    else:
        print("❌ Error al instalar el paquete.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python install_and_freeze.py <paquete>")
    else:
        install_package(sys.argv[1])

#ejecuar con python install_and_freeze.py fastapi
# con esto, si instalamos una nueva libreria, la registramos 
# en requirements.txt
