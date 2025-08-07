def test_imports():
    print("🔍 Verificando imports y rutas...")

    try:
        from fastapi import FastAPI
        from routers.Personas import Personas_router  # 👈 SIN app.
        
        app = FastAPI()
        app.include_router(Personas_router.router)

        routes = [route.path for route in app.routes]
        print("✅ Rutas registradas en la app:")
        for r in routes:
            print(f"   - {r}")

        print("🎉 Todos los imports y rutas funcionan correctamente.")

    except Exception as e:
        print("❌ ERROR al importar o registrar rutas:")
        print(str(e))
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_imports()
