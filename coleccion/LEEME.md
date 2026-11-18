# Colección de videos de mercancía de @delcarmen__1

Sus tomas originales (sin su cara). Qué hay en cada una y en qué segundos: `inventario.json`.

En una sesión nueva, para que los planes de `ediciones/` encuentren los clips:

    .venv/bin/python scripts/restaurar-coleccion.py

Copia cada archivo a su alias (`videos/clip-*.mov`) y genera las versiones limpias 1080x1920 (con los logos borrados).
Cuando ella mande videos nuevos de mercancía: guárdalos aquí, agrégalos a `inventario.json` y a `limpias` en el script.
