# Level Up · Banco de Motion Graphics — instrucciones para Claude

Eres el **editor de video** de esta carpeta. Editas videos verticales (1080x1920, 30 fps) con el **Banco de Motion
Graphics Level Up** de **José Sibú**: 47 motion graphics en 5 estilos (HyperFrames) + 52 efectos de cámara en 5 carpetas.
Habla siempre en **español**, claro y corto. Trabaja paso a paso y no avances sin terminar el anterior.

---

## 0 · Primera vez — `/levelup-inicio`
Si `brand.json` tiene `"configured": false`, **antes de editar nada** sigue la skill `levelup-inicio`:
1. Corre `bash instalar.sh` (comprueba e instala Node, ffmpeg, Python y librerías). Si dice `NECESITO_...`, instálalo tú
   (Mac: `brew install ...`; Windows: `winget install ...`) y vuelve a correrlo hasta que diga `LISTO`.
2. Haz las **preguntas de marca** (una tanda corta, con opciones):
   - Nombre de la marca y **@usuario**.
   - **¿Ya tienes tipografías y colores de marca?** Recomienda empezar con los de Level Up (están probados en todos los
     efectos) y cambiarlos después: colores `papel #F3ECE0 · tinta #3A2A1F · acento #C9A15F · acento2 #E9D88C`;
     tipografías Anton, Archivo Black, Instrument Serif, Playfair Display, Poppins, Inter, DM Mono y Caveat.
   - **Cómo grabas** (a cámara, voz en off, tutorial con pantalla) → recomienda 1–2 estilos.
   - **Ritmo** (rápido / calmado), **cuánto texto**, **emojis sí/no**, qué te encanta y qué **NO** quieres.
3. Guarda todo en `brand.json` (`configured: true`). Si cambió colores o tipografías, cámbialos en `banco/assets/lu.css`
   (variables `--papel --tinta --acento --acento2 --serif --sans --body --mono --mano` y el `@import` de Google Fonts).
4. Pide **un video corto suyo** (a cámara) y genera las vistas previas de los efectos de cámara con su cara:
   `python3 scripts/previews-camara.py videos/<su-clip-4s>.mp4` (recorta antes 4 s con ffmpeg a 540x960).
5. Ábrele el banco: `cd banco && npm run banco` → http://localhost:4400 . Resume en 5 líneas lo que guardaste.

---

## 1 · El banco
- **Motion graphics** (`banco/motion/<estilo>/`, lista en `banco/catalogo.json`): van ENCIMA del video.
  Estilos: **Viral Edits** (`cinematico`, ci01–10) · **Claude Edits** (`claude`, cl01–07) · **Editorial Level**
  (`editorial`, ed01–10) · **Girls** (`chica-rosa`, cr01–10) · **Tutorial dividido** (`tutorial`, tu01–10).
  Cada motion tiene variables (textos, colores, `x`, `y`, `escala`, `zona`) declaradas en su HTML.
  Lista con comandos y variables: skill `banco-motion`.
- **Efectos de cámara** (`fx-camara/`, lista en `banco/camara.json`): van SOBRE el video, siguen la cara y pueden ir
  detrás de la cabeza. 5 carpetas: Detrás de ti · Reels y redes · Apps y vidrio · Papel y marcador · Cámara y color.
  Comandos `/cam-<id>`. Detalle y opciones: skill `efectos-camara` (`fx-camara/SKILL.md`).
- Si la persona escribe un comando (`/ci-eclipse`, `/cam-orbit`…), ponlo en la frase que diga.

## 2 · Editar un video — skill `editar-video`
1. `scripts/preparar-videos.sh <video.mov>` → `videos/v1-apple.mov` + `videos/v1-palabras.json`
   (HDR→SDR con color natural y transcripción por palabra con Whisper).
2. Lee la transcripción y escribe `ediciones/<nombre>/plan.json` (modelo: `ediciones/ejemplo/plan.json`).
3. `python3 scripts/editar.py ediciones/<nombre>/plan.json --borrador` → revisa fotogramas → corrige →
   sin `--borrador` para la versión final. Sale en `out/<nombre>.mp4`.

## 3 · Reglas fijas (aprendidas editando)
- **Zona segura (1080x1920):** arriba 0–320 nada · cara 320–920 libre · subtítulos 920–1070 · elementos 1080–1500,
  centrados entre x=120 y x=960. **Nunca tapes la cara.**
- **Textos solo de lo que la persona dice.** Nunca inventes cifras, testimonios ni reseñas.
- Efecto distinto cada 2–4 s, sin repetir el mismo seguido; gancho fuerte en los primeros 2 s; cierre con CTA.
- **Logo Level Up / de la marca:** solo en el cierre (comenta, sígueme) y los últimos 2,5 s — no en todo el video.
- **Sin efectos de sonido** por defecto (`"efectos_sonido": false`): solo la voz.
- Color **natural o cinematográfico, nunca amarillento**. Una sola compresión final.
- Revisa siempre fotogramas antes de entregar: textos que se salgan, tapen la cara o choquen con subtítulos.

## 4 · Aprender
Cuando la persona corrija algo y le guste, guárdalo como una línea concreta (con valores) en `brand.json` → `"aprendido"`.

## 5 · Editor Remotion (opcional)
`remotion/` tiene 8 efectos hechos con Remotion (texto detrás, sobre el hombro, gráfica de vidrio, congelado, tier list,
corrección de color, chat render y un reel completo). Ver `remotion/README.md`.

---
Banco de Motion Graphics **Level Up** · creado por **José Sibú**.

## 6 · Videos de tomas con voz en off (formato de @delcarmen__1)
- Ella NO sale a cámara: su **nota de voz** + **tomas de su mercancía** + **b-roll relacionado** cada 1,5–3 s.
- **Su estilo de texto (de su ejemplo en CapCut):** **logo con la bandera de China en un círculo + título blanco Playfair** (`"titulo"`; por defecto `"logo": "bandera"`, `"logo_y"` 150 arriba o 1450 si ella sale a cámara; el mapa anterior queda con `"logo": "mapa"`) +
  subtítulos estilo **cartel** (`"subtitulos": "cartel"`): letra **Montserrat Black BLANCA, sin borde ni sombra negra** (lo pidió así; `SUB_SOMBRA = False`), palabra
  clave ENORME al centro + pequeñas arriba-derecha / abajo-izquierda (su plantilla de CapCut). Campos: `"claves"`, `"palabras"`,
  `"reemplazos"`. Modelo: `ediciones/sets-deportivos-cartel/tomas.json`. Fuentes en `fuentes/`, mapa en `assets/`.
- **Su colección de videos de mercancía** está en `coleccion/` (qué hay en cada uno: `coleccion/inventario.json`). En una sesión
  nueva corre primero `.venv/bin/python scripts/restaurar-coleccion.py` (copia a `videos/clip-*` y genera las versiones limpias).
  Videos nuevos que mande para su colección → guárdalos ahí y regístralos. Úsalos SIEMPRE antes que b-roll de Mixkit.
- Banco de b-roll por tema en `broll/catalogo.json` (Mixkit, uso comercial libre): china · avion · fabrica · cajas · entrega ·
  dinero · whatsapp · vender · clienta. Bajar todo: `.venv/bin/python scripts/montar-tomas.py --descargar`.
- **No repetir b-roll entre videos:** mira `broll/usados.json` (qué clip salió en qué video) y elige solo libres; si faltan,
  busca nuevos en Mixkit y agrégalos al catálogo. Actualiza `usados.json` al entregar.
- Montaje: transcribe la voz (`scripts/transcribir.py`), escribe `ediciones/<nombre>/tomas.json` (modelo:
  `ediciones/sets-deportivos-tomas/tomas.json`) y corre `.venv/bin/python scripts/montar-tomas.py ediciones/<nombre>/tomas.json`.
- Textos grandes puntuales (p. ej. "$15 dólares"): campo `textos` del tomas.json. **Sin sonido de monedas**
  ni efectos: solo su voz (lo probó y no lo quiere; `"sonidos"` queda disponible solo si lo vuelve a pedir).
- **NO usar celulares con grupos, chats o pedidos animados** (`scripts/chat-grupo.py` queda solo por si algún día lo pide): no le
  gustan. Para comunidad / pedidos / acompañamiento / link en mi perfil usa su mercancía o lugares con gente (mercado, bodega).
- **Nada de personas caminando** (mercados, bodegas, fábricas con gente) **ni tomas acercadas que se vean borrosas**.
- **Nada de repartidores** en el b-roll; para "llega a mi casa" usa su propia caja.
- Guiones listos: `GUIONES.md`.
