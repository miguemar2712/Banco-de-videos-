---
name: banco-motion
description: Lista de los 47 motion graphics del Banco Level Up (5 estilos) con su comando y sus variables. Úsala cuando pidan un motion por comando (/ci-eclipse, /ed-circulo…) o un motion graphic del banco.
---

# Motion graphics · Banco Level Up (José Sibú)

Van ENCIMA del video. En el plan: `{"id": "ci01", "t": 3.2, "dur": 3, "vars": {...}}` (t = segundo del video original).
Todas aceptan `x`, `y`, `escala`, `zona` (elementos | titulo | pantalla | libre), `fondo` (hoja | transparente) y los colores `papel tinta acento acento2`.
Vista previa: `cd banco && npm run banco` → http://localhost:4400

## Viral Edits (`cinematico`)
_Voz en off · lanzamientos, masterclass_ — Base oscura con resplandor dorado tipo eclipse, tarjetas de vidrio, interfaces animadas (prompt, terminal, línea de tiempo) y texto 3D.

| id | Comando | Nombre | Para qué | Variables propias |
|---|---|---|---|---|
| ci01 | `/ci-eclipse` | Eclipse de lanzamiento | Pantalla de lanzamiento: anillo de luz dorada + título brillante. | `etiqueta`, `titulo`, `sub` |
| ci02 | `/ci-prompt` | Barra de prompt | Se escribe una instrucción y se envía ("y en un solo prompt…"). | `titulo`, `prompt` |
| ci03 | `/ci-timeline` | Línea de tiempo | Editor con clips: se borran las tomas malas y se juntan las buenas. | `titulo` |
| ci04 | `/ci-lista` | Tarjeta de vidrio con lista | Lista que se marca al ritmo de lo que dices. | `titulo`, `items`, `ritmo` |
| ci05 | `/ci-3d` | Texto 3D dorado | Palabra en 3D que gira y entra desde el fondo. | `palabra` |
| ci06 | `/ci-pasos` | Pasos 1·2·3 | Tres pasos en vidrio, uno por uno. | `p1`, `p2`, `p3`, `ritmo` |
| ci07 | `/ci-ventana` | Ventana de Claude Code | Terminal que escribe lo que Claude va haciendo. | `app`, `lineas` |
| ci08 | `/ci-insignia` | Insignia "Editado por Claude" | Tarjeta con barra de render que llega a 100%. | `arriba`, `texto` |
| ci09 | `/ci-cta` | Tarjeta CTA | Cierre: tarjeta + botón dorado con brillo ("Comenta CLAUDE"). | `etiqueta`, `titulo`, `detalle`, `boton` |
| ci10 | `/ci-anillo` | Anillo de progreso | Número dentro de un anillo que se llena (%). | `valor`, `sufijo`, `texto` |

## Claude Edits (`claude`)
_Efectos de la guía · sobre cualquier estilo_ — Los 8 efectos de la guía de Claude: gráfica de vidrio, ranking, palabra detrás, tarjetas sobre los hombros, congelado tipo sticker, corrección de color y la intro de chat.

| id | Comando | Nombre | Para qué | Variables propias |
|---|---|---|---|---|
| cl01 | `/glass-graph` | Glass Graph | Tarjeta de vidrio en el pecho: número que sube y gráfica naranja que se dibuja. | `titulo`, `desde`, `hasta` |
| cl02 | `/tier-list` | Tier List | Ranking S-A-B-C-D que se llena solo, con "Clasificando…" → "Clasificado ✓". | `tema`, `S`, `A`, `B`, `C`, `D` |
| cl03 | `/text-behind` | Text Behind | Palabra gigante DETRÁS de tu cabeza. En el plan: "detras": true. | `palabra`, `cabeza`, `blanco` |
| cl04 | `/over-the-shoulder` | Over The Shoulder | Tarjetas ANTES/DESPUÉS detrás de tus hombros. En el plan: "detras": true. | `antesLabel`, `antesNumero`, `antesUnidad`, `despuesLabel`, `despuesNumero`, `despuesUnidad`, `hombros` |
| cl05 | `/freeze-frame` | Freeze Frame (etiqueta) | Flash + tu nombre. En el plan junto con el zoom "congelar" (imagen tipo sticker). | `nombre`, `rol`, `pecho` |
| cl06 | `/color-grade` | Color Grade (barrido) | Línea de luz + ANTES/DESPUÉS. En el plan junto con el zoom "grade". | `antes`, `despues` |
| cl07 | `/chat-render` | Chat Render (intro) | Intro tipo chat: escribes el comando, se envía y el resultado se "renderiza". | `comando`, `descripcion`, `miniatura`, `resultado` |

## Editorial Level (`editorial`)
_Hablando a cámara · marca personal, educación, lifestyle_ — Serif elegante en cursiva + letra gruesa, beige, café y oro. Texto encima de la cabeza, tarjetas tipo póster y detalles hechos a mano.

| id | Comando | Nombre | Para qué | Variables propias |
|---|---|---|---|---|
| ed01 | `/ed-titular` | Titular editorial | Gancho de los primeros 2 s: línea fuerte + palabra elegante + línea fuerte. | `arriba`, `centro`, `abajo` |
| ed02 | `/ed-palabra` | Palabra con resaltador | Una palabra clave centrada sobre la hoja con trazo de resaltador. | `antes`, `palabra`, `nota` |
| ed03 | `/ed-circulo` | Palabra clave a mano | La palabra en cursiva con un círculo dibujado a mano y una nota. | `palabra`, `nota` |
| ed04 | `/ed-tarjetas` | Tarjetas póster | Explicar 3 tipos/ideas: cada tarjeta cae cuando la nombras. | `t1`, `c1`, `t2`, `c2`, `t3`, `c3` |
| ed05 | `/ed-numero` | Número + título | "3 tipos de contenido", "5 errores": número gigante en oro. | `numero`, `cursiva`, `fuerte` |
| ed06 | `/ed-rec` | Marco de cámara REC | Momento "detrás de cámara" o confesión. Combínalo con el video en blanco y negro. | `calidad`, `blanco` |
| ed07 | `/ed-calendario` | Calendario con meta | Fechas, plazos, "antes de fin de año": marca el día a mano. | `anio`, `mes`, `dia`, `nota` |
| ed08 | `/ed-reloj` | Reloj que corre | Tiempo perdido o ahorrado ("horas editando"). | `frase`, `palabra`, `vueltas` |
| ed09 | `/ed-contador` | Contador | Resultados reales: vistas, ventas, alumnos. Solo cifras que la persona dice. | `arriba`, `prefijo`, `valor`, `sufijo`, `abajo` |
| ed10 | `/ed-cierre` | Cierre Instagram | Últimos 3 s: se oscurece, logo de Instagram, @usuario y frase final. | `usuario`, `frase` |

## Girls (`chica-rosa`)
_Hablando a cámara · branding femenino_ — Beige rosado con café vino, letra a mano, píldoras con check, pasos 01·02·03, antes/ahora y burbujas de comentario.

| id | Comando | Nombre | Para qué | Variables propias |
|---|---|---|---|---|
| cr01 | `/cr-portada` | Portada de serie | "bienvenida a la PARTE 02": portada con letra a mano y estrellas. | `arriba`, `titulo`, `tag` |
| cr02 | `/cr-pildoras` | Píldoras con check | Lista de píldoras que aparecen una por una. | `items`, `ritmo`, `lado` |
| cr03 | `/cr-gigante` | Texto gigante | Dos líneas gigantes que entran de lados opuestos. | `linea1`, `linea2` |
| cr04 | `/cr-numero` | Número + palabra | "5 HORAS" con nota a mano. | `numero`, `palabra`, `nota` |
| cr05 | `/cr-paleta` | Paleta de marca | Tus colores y tipografías ("mis colores"). | `colores`, `titulo` |
| cr06 | `/cr-paso` | Paso 01 con captura | Número + título a mano + marco con tu captura. | `numero`, `titulo`, `tag`, `imagen` |
| cr07 | `/cr-antes-ahora` | Antes / Ahora | Dos tarjetas con flecha: antes y después. | `antes`, `ahora`, `pie1`, `pie2`, `imagen1`, `imagen2` |
| cr08 | `/cr-etiquetas` | Etiquetas flotantes | Etiquetas que aparecen alrededor mientras las nombras. | `items`, `final` |
| cr09 | `/cr-comenta` | Comenta + burbuja | CTA: palabra en burbuja de chat + etiqueta. | `arriba`, `palabra`, `tag` |
| cr10 | `/cr-polaroid` | Polaroid volando | Foto/captura tipo polaroid con cinta que entra volando. | `pie`, `imagen`, `lado` |

## Tutorial dividido (`tutorial`)
_Pantalla dividida · paso a paso_ — Pantalla dividida: gráficos arriba sobre hoja cuadriculada y tu cámara abajo. Ventanas, celular, gráficas, mapa mental.

| id | Comando | Nombre | Para qué | Variables propias |
|---|---|---|---|---|
| tu01 | `/tu-portada` | Portada pregunta | "¿Cómo empezar en ___?" con barras que suben. | `pregunta`, `tema`, `chip` |
| tu02 | `/tu-paso` | Paso con progreso | PASO 1 + título + puntitos de progreso. | `paso`, `total`, `titulo`, `detalle` |
| tu03 | `/tu-web` | Página web | Navegador que escribe la dirección y carga. | `url`, `marca`, `sub` |
| tu04 | `/tu-celular` | App en el celular | Celular sube, descarga la app y queda lista. | `app`, `icono`, `titulo` |
| tu05 | `/tu-apps` | App + App | Dos apps con + y "solo necesitas estas 2". | `app1`, `ico1`, `uso1`, `app2`, `ico2`, `uso2`, `chip` |
| tu06 | `/tu-opciones` | Elige una opción | 4 opciones, se marca una y se escribe la búsqueda. | `titulo`, `opciones`, `elegida`, `nota`, `busca` |
| tu07 | `/tu-grafica` | Gráfica de velas | Velas que se dibujan + marcas de techo y piso. | `titulo`, `par`, `techo`, `piso` |
| tu08 | `/tu-mapa` | Mapa mental | Centro + ramas que se dibujan. | `centro`, `ramas` |
| tu09 | `/tu-barras` | Número + barras | Número que sube con barras y una destacada. | `etiqueta`, `valor`, `texto` |
| tu10 | `/tu-referencias` | Tablero de referencias | 3 tarjetas de referencia con notas a mano en rojo. | `titulo`, `tarjetas`, `notas` |
