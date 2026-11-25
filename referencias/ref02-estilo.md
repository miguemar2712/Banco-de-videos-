# Estilo REF 02 — notas completas (de `ref02-guia-visual.pdf`)

Usar este documento como **especificación de estilo**, no como guion. Formato de salida: **1080x1920, 30 fps, H.264 + AAC**.
Referencia original: 27,7 s, 9:16 (512x910). Adaptar los segundos del mapa al audio nuevo.

## 1 · ADN visual
1. **Editorial comercial:** montaje vertical de producto y experiencia; el texto superpuesto guía la historia.
2. **Título de alto impacto:** MAYÚSCULAS muy pesadas, **crema #FFF0AF**, sombra oscura discreta.
3. **Contraste tipográfico:** segunda línea en **serif cursiva BLANCA**, solapada con el titular.
4. **Subtítulos cinéticos:** frases blancas sans serif que cambian por palabras y **crecen en términos clave**.
5. **Etiquetas / alertas:** **stickers rosados colgantes de precio** sobre los productos, siempre legibles.
6. **Montaje por objeto:** cortes entre producto, unboxing, lugar y prueba de entrega o uso.

## 2 · Tipografía (tamaños en lienzo 1080x1920)
| Capa | Fuente (equivalentes) | Tamaño | Detalles |
|---|---|---|---|
| A · Titular | **Anton**, League Spartan Black o Montserrat ExtraBold/Black | 90–135 px | MAYÚSCULAS, tracking −2 % a −4 %, interlineado compacto, sombra suave. Color crema #FFF0AF |
| B · Serif cursiva | **Playfair Display Bold Italic**, DM Serif Display Italic o Libre Baskerville Italic | 50–85 px | Blanca, sobre o debajo del titular, solapada |
| C · Subtítulos | **Montserrat SemiBold/ExtraBold**, Inter Bold o Poppins Medium/Bold | 45–70 px | Blancos. Peso medio para conectores, negrita para cifras y verbos |
| Cifra | Pesada (como titular) | 90–130 px | Ej. "**$200** *de ganancia*" (cifra + cursiva) |

Ejemplo del PDF: **INVERTI** (crema, pesada) + *solamente $180* (blanca, cursiva serif).
No hay fuente exacta identificable: usar las equivalentes, sin prometer copia pixel-perfect.

## 3 · Colores
| HEX | Nombre | Uso |
|---|---|---|
| `#FFF0AF` | Crema titular | Títulos grandes, palabras de alto valor, CTA |
| `#FFFFFF` | Blanco | Subtítulos, cifras, cursivas |
| `#171817` | Negro tinta | Sombra, contraste, overlays |
| `#F68CBF` | Rosa etiqueta | Alertas y stickers de precio |
| `#D56F35` | Naranja acento | Acentos ocasionales |
| `#7B7770` | Gris cálido | Separadores y elementos secundarios |

Textura: fotografía natural de interiores y productos, **sin filtro uniforme**. Títulos con sombra u oclusión leve.
**Evitar** brillos metálicos, neones y degradados excesivos.

## 4 · Mapa de montaje (referencia de 27,7 s — adaptar a la voz)
| Tiempo | Escena | Qué pasa |
|---|---|---|
| 0:00–1,8 | **Gancho** | Titular gigante + subtítulo fino (cursiva) + cifra, desde el primer fotograma |
| 1,8–3,9 | Producto / beneficio | Corte a detalle de producto; cifra de ganancia escalada |
| 3,9–5,8 | Localización | Cortes a exterior; subtítulos por palabra + acento tipográfico |
| 5,8–8,7 | Explicación | Vuelta al unboxing; palabras clave agrandadas |
| 8,7–13,8 | Catálogo rápido | Categorías en MAYÚSCULAS + stickers de precio; alternar productos |
| 13,8–16,0 | Empaque | Cajas/objetos con microtextos al ritmo del habla |
| 16,0–19,2 | Plataformas | Escena de entorno + insert de interfaz (mockup propio) |
| 19,2–21,4 | Promesa / entrega | Cambio de lugar y de plano; frase principal en bold |
| 21,4–23,4 | **CTA** | Llamada a la acción en **crema + cursiva, centrada** |
| 23,4–fin | Cierre | Fondo oscurecido (dim). Sin usuario ni iconos sociales |

## 5 · Efectos y motion (a 30 fps)
- **Titular pop-in:** escala 115 % → 100 % en 4–7 frames, ease-out; sombra negra con blur moderado; dura 0,6–1,8 s.
- **Subtítulos palabra por palabra:** revelar por palabra o grupitos; cambiar cada 0,15–0,55 s según la voz.
- **Cifra con punch:** entra un poco más grande que el texto, rebote mínimo; nunca deformar los números.
- **Cursiva superpuesta:** solapada bajo el titular; fade + desplazamiento vertical suave en 5–9 frames.
- **Corte a detalle:** cortes secos (hard cuts) a producto, empaque o escenario en cada cambio de idea; sin transiciones decorativas.
- **Micro zoom en b-roll:** 100 % → 103–106 %, sutil, sin perder foco.
- **Sticker de precio:** etiqueta colgante **rosa #F68CBF**, rotación −8° a +8°, pop + microrebote, texto blanco grande con la cifra.
- **Cuerda de etiqueta:** línea fina o asa encima del sticker; escala proporcional al producto.
- **Carteles por categoría:** título crema en MAYÚSCULAS sobre la ropa/objetos; entra en el corte o con pop corto; sale al cambiar de categoría.
- **Insert de interfaz:** ventana/captura de plataforma en miniatura con sombra y bordes limpios (mockup propio, sin logos ajenos).
- **Match cut:** cambiar de toma cuando se levanta un objeto, aparece una mano, se mueve una bolsa o gira la cámara.
- **Whip / desenfoque corto:** 3–5 frames, solo si motiva el cambio (en la referencia, una sola vez cerca del 75 %).
- **Dim-overlay final:** oscurecer el fondo progresivamente 50–70 % para el CTA.

## 6 · Maquetas 9:16
1. **Gancho:** TITULAR crema arriba + *editorial* cursiva blanca debajo; caja de PALABRA CLAVE más abajo.
2. **Producto:** PRODUCTO en crema bajo la toma + sticker rosa "$5" inclinado a la derecha.
3. **CTA limpio:** COMENTA (crema) + *palabra clave* (cursiva blanca) en el centro, fondo oscurecido.

Zona segura: margen lateral 80–100 px; nada de subtítulos sobre los controles de TikTok/IG ni texto importante en la franja de abajo.

## 7 · Pipeline
1. Transcribir la voz con tiempos por palabra y momentos enfáticos.
2. Elegir b-roll sincronizado con el significado (su mercancía primero).
3. Presets: **HeadlineCream, SerifOverlay, KineticCaption, PriceTag, CTA**.
4. Animar: pop 4–7 frames · easing 5–9 frames · blur 3–5 frames.
5. Capas (de abajo arriba): video → sombreado local → etiquetas → subtítulos → títulos → efectos.
6. Sonido: voz clara; cortes en sílabas/pausas. (En este proyecto: **sin efectos de sonido**, ver `brand.json`.)
7. Exportar H.264 1080x1920 30 fps AAC; revisar overlays y márgenes.

## 8 · Prompt maestro (resumen de reglas)
- **Primero una tabla de escenas**: timestamp, toma, texto, efecto, keyframes, duración, audio. Luego editar y sacar vista previa.
- Revisar sincronización, legibilidad, **ortografía** y márgenes antes de entregar.
- Cada efecto **solo donde la narración lo justifique**.
- **NO** marca de agua LEVEL UP ni ninguna otra; **NO** rostros, nombres, usuarios ni iconos de Instagram del video de referencia; **NO** logos de marcas de productos; **NO** capturas de la referencia.
- Solo archivos de ella o gráficos neutrales propios. Si falta material: placeholder neutral y avisar; nunca inventar clips.
- Criterio de aceptación: que evoque el estilo dinámico del ejemplo con composiciones 100 % nuevas.
