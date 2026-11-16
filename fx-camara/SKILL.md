---
name: efectos-camara
description: Efectos de cámara del Banco de Motion Graphics Level Up (52 efectos en 5 carpetas) que siguen la cara y pueden ir detrás de la persona. Úsala cuando pidan /cam-<efecto>, un efecto de cámara, o uno de estos efectos por su nombre.
---

# Efectos de cámara · Level Up (José Sibú)

52 efectos que se aplican SOBRE el video de la persona (no encima como los motion graphics): siguen su cara, recortan
su silueta y pueden ir detrás de su cabeza. Sin sonidos. Habla en español, claro y corto.

## Cómo se usan en una edición
En `ediciones/<nombre>/plan.json`:
```json
"camara_fx": [
  {"fx": "glitter-spotlight", "t": 21.6, "dur": 2.4, "text": "CLAUDE"},
  {"fx": "apple-toggles", "t": 42.3, "dur": 4.6, "text": "Sonidos|Ruidos|Zoom", "ticks": "42.6|43.3|44.1"}
]
```
- `t` = segundo del video ORIGINAL (búscalo en la transcripción); `dur` en segundos (1,5–4 s se ve mejor).
- `ticks` y `at` también en segundos del video original: `editar.py` los convierte solo.
- `"ocultar_subs": true` esconde los subtítulos mientras dura el efecto (automático en checklist, gráfica de vidrio y cinta).
- Nunca tapes la cara: si un fotograma de revisión lo muestra, cambia `x`/`y` o acorta el texto.
- Textos siempre de lo que la persona dice. Cifras reales, nunca inventadas.

Probar un efecto suelto: `python3 fx-camara/scripts/fx.py orbit video.mp4 salida.mp4 --start 3 --end 6 --text "..."`
Fotograma de revisión: añade `--still 4.5` y una salida `.png`.

## Los 52 efectos (5 carpetas)

### 📁 Detrás de ti
_Palabras, letreros y portadas gigantes detrás de tu cabeza_

| Comando | `fx` | Qué hace | Opciones (en inglés, tal cual) |
|---|---|---|---|
| `/cam-backdrop-word` | `backdrop-word` | **Palabra detrás** · Palabra gigante que cae detrás de ti | `text`, `color` (hex), `font` (`bold` or `serif`) |
| `/cam-spotlight` | `spotlight` | **Foco** · Se apagan las luces y solo tú quedas iluminado | `text` (glowing word behind you), `color`, `push` |
| `/cam-glitter-spotlight` | `glitter-spotlight` | **Foco dorado** · Rayos dorados y destellos detrás de tu cabeza | `text` (glowing word behind you), `color`, `push` |
| `/cam-cover-star` | `cover-star` | **Portada de revista** · Te vuelves portada de revista | `text` (title), `lines` (with `\|`), `issue`, `color` |
| `/cam-red-collage` | `red-collage` | **Collage rojo** · Tú en blanco y negro, palabra roja gigante detrás | `text` (red word), `lines` (with `\|`), `tag` |
| `/cam-pastel-word` | `pastel-word` | **Palabra pastel** · Cuarto lavanda, palabra gigante y tarjeta de perfil | `text`, `name`, `handle` |
| `/cam-match-cut` | `match-cut` | **Corte de noticias** · Páginas de noticias que cortan en una palabra | `text` (the word, default Claude), `color` |
| `/cam-led-sign` | `led-sign` | **Letrero LED** · Se apagan las luces y un letrero LED se escribe | `text` (lines with `\|`), `color`, `push` |
| `/cam-select-resize` | `select-resize` | **Seleccionar y agrandar** · Una caja azul agarra tu número y lo agranda | `text` (default 2X) |
| `/cam-huge-strike` | `huge-strike` | **Palabra tachada** · Palabra gigante detrás que se tacha | `text`, `at` (seconds into the effect when the strike lands, default 0.6) |
| `/cam-crayon-write` | `crayon-write` | **Crayón** · Un crayón rojo escribe tu palabra detrás | `text` |

### 📁 Reels y redes
_Tus reels, tu perfil, comentarios, mensajes y el botón de seguir_

| Comando | `fx` | Qué hace | Opciones (en inglés, tal cual) |
|---|---|---|---|
| `/cam-noise` | `noise` | **Ruido de reels** · Tus reels se apilan detrás de tu cabeza | `images` (folder of screenshots or clips), `size` |
| `/cam-orbit` | `orbit` | **Órbita** · Tus reels giran alrededor de tu cabeza | `images`, `count`, `speed`, `size` |
| `/cam-comment-box` | `comment-box` | **Caja de comentario** · Un comentario de Instagram se escribe solo | `text` (default EFFECTS) |
| `/cam-tap` | `tap` | **Botón Seguir** · El botón Seguir pasa a Siguiendo | `at` (video second of the flip), `x`, `y` (0 to 1), `color` |
| `/cam-reel-frame` | `reel-frame` | **Marco de reel** · Tu video se encoge a una tarjeta de reel | `text` (handle) |
| `/cam-profile-wall` | `profile-wall` | **Muro de perfil** · Tus reels llenan la pared con un contador | `images`, `count`, `label` |
| `/cam-phone-fan` | `phone-fan` | **Abanico de teléfonos** · Tus reels en abanico como cartas | `images`, `text` (lines with `\|`) |
| `/cam-carousel-spin` | `carousel-spin` | **Carrusel 3D** · Tus reels giran alrededor de ti en 3D | `images`, `count`, `size`, `turns` |
| `/cam-messages` | `messages` | **Mensajes** · Notificaciones de iMessage una tras otra | `text` (messages with `\|`), `title` (default Messages), `y` |
| `/cam-place-in-grid` | `place-in-grid` | **En tu perfil** · Te encoges al centro de tu perfil de 3x3 | `images` (folder of your reels or covers), `views` (9 counts with `\|`, the 9th is yours) |
| `/cam-fan-build` | `fan-build` | **Abanico de portadas** · Tus portadas se reparten en abanico detrás | `images` (folder of your covers), `count` (default 13) |

### 📁 Apps y vidrio
_Interfaces tipo iPhone y Claude: vidrio, gráficas, listas y terminal_

| Comando | `fx` | Qué hace | Opciones (en inglés, tal cual) |
|---|---|---|---|
| `/cam-the-bill` | `the-bill` | **Ticket** · Tus instrucciones se imprimen como un ticket | `text` (lines joined with `\|`) |
| `/cam-todo` | `todo` | **Lista de tareas** · Lista junto a tu cabeza que se va marcando | `text` (items with `\|`), `ticks` (video seconds with `\|`), `title` |
| `/cam-glass-widgets` | `glass-widgets` | **Widgets de vidrio** · Widgets de vidrio flotando alrededor de tu cabeza | `text` (big number), `name`, `handle`, `look` (`simple` for the 3-widget version) |
| `/cam-timeline` | `timeline` | **Línea de tiempo** · Look de película con línea de edición y REC | `text` (title), `sub`, `tc` |
| `/cam-tier-list` | `tier-list` | **Tier list** · Una tier list y Claude vuela a la S | `title`, `item`, `others` |
| `/cam-checklist` | `checklist` | **Checklist de Claude** · Lista de tareas de Claude bajo tu barbilla | `text` (`step::meta\|...`), `title` |
| `/cam-liquid-glass-graph` | `liquid-glass-graph` | **Gráfica de vidrio** · Tarjeta de vidrio con gráfica que sube | `text` (label), `from`, `to` (e.g. `197K`, `59%`), `color` |
| `/cam-apple-toggles` | `apple-toggles` | **Interruptores iPhone** · Interruptores de iPhone que se encienden | `text` (rows with `\|`), `ticks` (seconds with `\|`), `color` |
| `/cam-over-the-shoulder-zoom` | `over-the-shoulder-zoom` | **Sobre el hombro** · La cámara va a una esquina y aparece una gráfica | `text` (two labels with `\|`), `to` (two numbers with `\|`, e.g. `197K\|672K`), `zoom` (default 2.0) |
| `/cam-wave-trim` | `wave-trim` | **Recorte de voz** · Los silencios de tu voz se recortan en pantalla | none |

### 📁 Papel y marcador
_Look editorial hecho a mano: marcador, cinta, sellos y titulares_

| Comando | `fx` | Qué hace | Opciones (en inglés, tal cual) |
|---|---|---|---|
| `/cam-lineup` | `lineup` | **Fila numerada** · Tarjetas numeradas en abanico sobre tu cabeza | `text` (tile names joined with `\|`) |
| `/cam-pause-point` | `pause-point` | **Pausa y flecha** · Congela la imagen y te señala con una flecha | `text` (label), `color`, `label_x` |
| `/cam-reject-stamp` | `reject-stamp` | **Sello** · Un sello rojo cae de golpe | `text`, `color`, `angle`, `y` |
| `/cam-countdown-flip` | `countdown-flip` | **Cuenta regresiva** · Reloj 3, 2, 1 sobre tu cabeza | `from` |
| `/cam-scribble` | `scribble` | **Garabatos** · Garabatos de marcador alrededor de ti | `text` (label), `color` |
| `/cam-split-headline` | `split-headline` | **Titular dividido** · Un titular baja y te empuja a la mitad de abajo | `text` (lines with `\|`), `hl` (highlighted word), `pill` |
| `/cam-check-pills` | `check-pills` | **Píldoras con clic** · Hoja cuadriculada, reels detrás, un cursor hace clic | `text` (pills with `\|`), `images` |
| `/cam-headline-box` | `headline-box` | **Titular en caja** · Zoom con titular de dos líneas | `text` (lines with `\|`), `zoom` |
| `/cam-headline-wall` | `headline-wall` | **Muro de titulares** · Tus titulares se apilan detrás y aparece un total | `text` (`headline::meta\|...`), `total`, `label` |
| `/cam-tape-label` | `tape-label` | **Cinta** · Una cinta amarilla con tu frase en el pecho | `text` |

### 📁 Cámara y color
_Movimientos de cámara, zooms, color y transiciones_

| Comando | `fx` | Qué hace | Opciones (en inglés, tal cual) |
|---|---|---|---|
| `/cam-locked-on` | `locked-on` | **Fijado** · Corchetes se fijan en tu cara y la cámara te sigue | `zoom` (default 1.35), `text` (tag) |
| `/cam-lean-in` | `lean-in` | **Acercamiento** · Zoom rápido en una palabra | `zoom` (default 1.45, max 2), `speed` |
| `/cam-moody` | `moody` | **Color moody** · Corrección de color oscura y cinematográfica | `grade` (`moody`, `bw`, `warm`, `cool`, `pop`) |
| `/cam-swipe` | `swipe` | **Antes y después** · Barra que desliza del antes al después | `grade` (the "after" look) |
| `/cam-uninstall` | `uninstall` | **Desinstalar** · Barra de desinstalar con glitch | `text` |
| `/cam-shortcut-rain` | `shortcut-rain` | **Lluvia de teclas** · Teclas que llueven detrás de ti | `text` (keys with `\|`), `count` |
| `/cam-rabbit-hole` | `rabbit-hole` | **Túnel** · La imagen se mete en sí misma girando | `ratio`, `speed`, `spin` |
| `/cam-broll-split` | `broll-split` | **B-roll dividido** · B-roll arriba con etiqueta, tú abajo | `images`, `text` (tag) |
| `/cam-dot-reveal` | `dot-reveal` | **Puntos** · Tu imagen se arma con puntos brillantes | `color`, `cell` |
| `/cam-slow-push` | `slow-push` | **Empuje lento** · Zoom lento de cine con el fondo desenfocado | `zoom` (default 1.6), `blur` |
