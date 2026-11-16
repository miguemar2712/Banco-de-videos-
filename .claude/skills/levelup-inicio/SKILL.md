---
name: levelup-inicio
description: Primera vez con el Banco de Motion Graphics Level Up — instala todo (Node, ffmpeg, Python, Whisper, MediaPipe, HyperFrames, Remotion opcional) y hace las preguntas de marca (colores, tipografías, @usuario, cómo grabas, gustos). Úsala si brand.json tiene "configured": false o la persona escribe /levelup-inicio.
---

# Primera vez · Level Up

Habla en español, claro y corto. No le pidas a la persona que corra comandos: hazlo tú.

## 1. Instala
1. `bash instalar.sh`. Si imprime `NECESITO_NODE`, `NECESITO_FFMPEG` o `NECESITO_PYTHON`, instálalo:
   - Mac: `brew install node ffmpeg python@3.12` (sin Homebrew: dile que lo instale desde brew.sh).
   - Windows: `winget install OpenJS.NodeJS.LTS`, `winget install ffmpeg`, `winget install Python.Python.3.12`.
   Vuelve a correr `bash instalar.sh` hasta ver `LISTO`.
2. Usa siempre `.venv/bin/python` (Windows: `.venv\Scripts\python.exe`) para los scripts de `scripts/`.
3. (Opcional, editor Remotion) `cd remotion && npm install`.

## 2. Pregunta la marca (una tanda corta, con opciones)
1. Nombre de la marca y @usuario de Instagram/TikTok.
2. **¿Ya tienes colores y tipografías de marca?**
   - Recomendación: empieza con los de Level Up, que están probados en todos los efectos, y cámbialos después.
   - Colores: papel `#F3ECE0`, tinta `#3A2A1F`, acento oro `#C9A15F`, acento suave `#E9D88C`.
   - Tipografías: Anton / Archivo Black (impacto), Playfair Display / Instrument Serif (elegante), Inter / Poppins (texto), DM Mono (interfaces), Caveat (a mano).
   - Si tiene las suyas, que sean de Google Fonts; propón 3 opciones según su vibra si no sabe.
3. ¿Cómo grabas? A cámara · voz en off · tutorial con pantalla. Recomienda 1–2 estilos:
   - A cámara, ritmo viral → **Viral Edits** + efectos de cámara.
   - Marca femenina → **Girls**.
   - Educativo → **Editorial Level** o **Tutorial dividido**.
   - Contenido de IA/Claude → **Claude Edits**.
4. Ritmo (rápido/calmado), mucho o poco texto, emojis sí/no, referencias que ama, y qué NO quiere.

## 3. Guarda y muestra
1. Escribe `brand.json` con todo, y `"configured": true`.
2. Si cambió colores o tipografías:
   - Cámbialos en `banco/assets/lu.css`: variables de `:root` y el `@import` de Google Fonts.
   - Cambia también los colores por defecto de `BASE` en `banco/galeria.html`.
3. Pídele un video corto a cámara. Saca 4 s con `ffmpeg -ss 2 -t 4 -i video -vf scale=540:960,fps=30 banco/assets/camara/_clip.mp4`. Genera las vistas previas con su cara: `.venv/bin/python scripts/previews-camara.py`.
4. Abre el banco: `cd banco && npm run banco` → http://localhost:4400.
5. Resume en 5 líneas lo que guardaste.
