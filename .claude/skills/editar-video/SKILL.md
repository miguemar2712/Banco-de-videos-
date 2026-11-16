---
name: editar-video
description: Edita un video vertical con el Banco de Motion Graphics Level Up — prepara (color + transcripción), corta pausas, elige motion graphics y efectos de cámara según lo que la persona dice, subtítulos, zooms, logo en el cierre, y renderiza. Úsala con /editar, "edítame este video" o cuando pasen un video.
---

# Editar un video · Level Up

Lee `brand.json` (marca, estilos, gustos, `aprendido`) antes de empezar. Habla en español.

## Pasos
1. **Preparar:**
   - `scripts/preparar-videos.sh "<video.mov>"` → `videos/vN-apple.mov` + `videos/vN-palabras.json`.
   - Para numerar desde otro número: `INICIO=4 scripts/preparar-videos.sh ...`.
2. **Leer** la transcripción completa y entender qué dice, frase por frase.
3. **Tramos:** elige las partes buenas (`tramos: [{de, a}]`, en segundos del original).
   - Quita repeticiones, errores y lo que sobra.
   - Corrige palabras mal escuchadas con `reemplazos` o con `texto` en el tramo.
   - Las pausas > `silencio` (0,3 s) se cortan solas; `mantener_pausas` para conservar alguna.
4. **Planifica** (tabla: segundo · lo que dice · efecto) y escribe `ediciones/<nombre>/plan.json`:
   - **Gancho** fuerte en los primeros 2 s.
   - Algo nuevo cada 2–4 s, sin repetir el mismo efecto seguido.
   - El efecto debe coincidir con **lo que se dice en ese momento** (lista → checklist/interruptores, "comenta" → caja de comentario, número → gráfica…).
   - `motions` (banco, encima del video): `{id, t, dur, vars, detras?, ocultar_subs?}`.
   - `camara_fx` (sobre el video, siguen la cara): `{fx, t, dur, text, ...opciones}`.
   - `zooms`: `golpe`, `suave`, `sacudida`, `flash`, `luz`, `byn`, `grade`, `congelar`, `marco`, `dividida`.
   - `claves`: palabras destacadas en los subtítulos (1 por frase como máximo).
   - **Cierre** con CTA (`ci09`, `cr09`, `ed10`, `/cam-comment-box`, `/cam-tap`): ahí aparece el logo.
5. **Borrador:**
   - `.venv/bin/python scripts/editar.py ediciones/<nombre>/plan.json --borrador`.
   - Saca fotogramas a mitad de cada efecto (`ffmpeg -ss T -i out/<nombre>-borrador.mp4 -frames:v 1 f.png`) y míralos.
   - Corrige textos que se salgan, tapen la cara o choquen con los subtítulos.
6. **Final:** el mismo comando sin `--borrador` → `out/<nombre>.mp4`. Dile qué decisiones tomaste (5 líneas).

## Reglas
- Zona segura: arriba 0–320 nada; cara 320–920 libre; subtítulos 920–1070; elementos 1080–1500 centrados (x 120–960).
- Cada motion acepta `x`, `y`, `escala`. Con `"detras": true` va detrás de la persona.
- Textos solo de lo que dice la persona. Nunca inventes cifras ni testimonios.
- Sin efectos de sonido salvo que los pida (`"efectos_sonido": true` + sonidos propios en `banco/assets/sonidos/`).
- Logo solo en el cierre (`"marca": "final"`, por defecto); `"siempre"` para todo el video, `false` para quitarlo.
- Cuando corrija algo y le guste, añádelo a `brand.json` → `aprendido`.
