#!/usr/bin/env python3
"""Genera las vistas previas de los 51 efectos de cámara (fx-camara/) para el banco.

uso: python3 scripts/previews-camara.py [clip.mp4] [--solo orbit,spotlight]
Sale en banco/assets/camara/<carpeta>/<id>.mp4 y banco/camara.json (lo lee la galería).
"""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
FX = os.path.join(RAIZ, 'fx-camara', 'scripts', 'fx.py')
SAL = os.path.join(RAIZ, 'banco', 'assets', 'camara')

# 5 carpetas por estilo visual (≈10 efectos cada una)
CARPETAS = [
    ('detras', 'Detrás de ti', 'Palabras, letreros y portadas gigantes detrás de tu cabeza',
     'backdrop-word spotlight glitter-spotlight led-sign huge-strike crayon-write red-collage pastel-word match-cut cover-star select-resize'),
    ('redes', 'Reels y redes', 'Tus reels, tu perfil, comentarios, mensajes y el botón de seguir',
     'noise orbit carousel-spin fan-build phone-fan profile-wall place-in-grid comment-box tap messages reel-frame'),
    ('apps', 'Apps y vidrio', 'Interfaces tipo iPhone y Claude: vidrio, gráficas, listas y terminal',
     'glass-widgets liquid-glass-graph over-the-shoulder-zoom apple-toggles checklist todo the-bill timeline wave-trim tier-list'),
    ('papel', 'Papel y marcador', 'Look editorial hecho a mano: marcador, cinta, sellos y titulares',
     'scribble pause-point tape-label reject-stamp check-pills headline-box split-headline headline-wall lineup countdown-flip'),
    ('camara', 'Cámara y color', 'Movimientos de cámara, zooms, color y transiciones',
     'locked-on lean-in slow-push moody swipe rabbit-hole dot-reveal uninstall shortcut-rain broll-split'),
]
GRUPO = {fid: c[0] for c in CARPETAS for fid in c[3].split()}

# id, nombre visible, qué hace, opciones de ejemplo (en español)
EFECTOS = [
    ('noise', 'Ruido de reels', 'Tus reels se apilan detrás de tu cabeza', {}),
    ('lineup', 'Fila numerada', 'Tarjetas numeradas en abanico sobre tu cabeza', {'text': 'Cortes|Subtítulos|Zoom|Color'}),
    ('locked-on', 'Fijado', 'Corchetes se fijan en tu cara y la cámara te sigue', {'text': 'CREADOR'}),
    ('orbit', 'Órbita', 'Tus reels giran alrededor de tu cabeza', {}),
    ('lean-in', 'Acercamiento', 'Zoom rápido en una palabra', {}),
    ('backdrop-word', 'Palabra detrás', 'Palabra gigante que cae detrás de ti', {'text': 'CLAUDE'}),
    ('spotlight', 'Foco', 'Se apagan las luces y solo tú quedas iluminado', {'text': 'CLAUDE'}),
    ('glitter-spotlight', 'Foco dorado', 'Rayos dorados y destellos detrás de tu cabeza', {'text': 'CLAUDE'}),
    ('the-bill', 'Ticket', 'Tus instrucciones se imprimen como un ticket', {'text': 'Corta las pausas|Pon subtítulos|Agrega zoom|Color de cine'}),
    ('moody', 'Color moody', 'Corrección de color oscura y cinematográfica', {}),
    ('swipe', 'Antes y después', 'Barra que desliza del antes al después', {}),
    ('todo', 'Lista de tareas', 'Lista junto a tu cabeza que se va marcando', {'text': 'Grabar|Subir a Claude|Publicar', 'title': 'Hoy'}),
    ('comment-box', 'Caja de comentario', 'Un comentario de Instagram se escribe solo', {'text': 'CLAUDE'}),
    ('tap', 'Botón Seguir', 'El botón Seguir pasa a Siguiendo', {}),
    ('pause-point', 'Pausa y flecha', 'Congela la imagen y te señala con una flecha', {'text': 'yo'}),
    ('uninstall', 'Desinstalar', 'Barra de desinstalar con glitch', {'text': 'Desinstalando CapCut'}),
    ('reel-frame', 'Marco de reel', 'Tu video se encoge a una tarjeta de reel', {'text': '@tu_usuario'}),
    ('shortcut-rain', 'Lluvia de teclas', 'Teclas que llueven detrás de ti', {}),
    ('reject-stamp', 'Sello', 'Un sello rojo cae de golpe', {'text': 'NO'}),
    ('countdown-flip', 'Cuenta regresiva', 'Reloj 3, 2, 1 sobre tu cabeza', {}),
    ('rabbit-hole', 'Túnel', 'La imagen se mete en sí misma girando', {}),
    ('cover-star', 'Portada de revista', 'Te vuelves portada de revista', {'text': 'LEVEL UP', 'lines': 'Edita con Claude|Sin CapCut|Gratis'}),
    ('scribble', 'Garabatos', 'Garabatos de marcador alrededor de ti', {'text': 'yo'}),
    ('glass-widgets', 'Widgets de vidrio', 'Widgets de vidrio flotando alrededor de tu cabeza', {'name': 'Level Up', 'handle': '@tu_usuario'}),
    ('red-collage', 'Collage rojo', 'Tú en blanco y negro, palabra roja gigante detrás', {'text': 'CLAUDE', 'lines': 'Corta|Edita|Publica'}),
    ('split-headline', 'Titular dividido', 'Un titular baja y te empuja a la mitad de abajo', {'text': 'Claude edita|tus videos', 'hl': 'Claude'}),
    ('pastel-word', 'Palabra pastel', 'Cuarto lavanda, palabra gigante y tarjeta de perfil', {'text': 'CLAUDE', 'name': 'Level Up', 'handle': '@tu_usuario'}),
    ('check-pills', 'Píldoras con clic', 'Hoja cuadriculada, reels detrás, un cursor hace clic', {'text': 'Subtítulos|Zoom|Color'}),
    ('timeline', 'Línea de tiempo', 'Look de película con línea de edición y REC', {'text': 'Editando', 'sub': 'con Claude'}),
    ('headline-box', 'Titular en caja', 'Zoom con titular de dos líneas', {'text': 'Esto lo editó|Claude'}),
    ('profile-wall', 'Muro de perfil', 'Tus reels llenan la pared con un contador', {'label': 'videos'}),
    ('tier-list', 'Tier list', 'Una tier list y Claude vuela a la S', {'title': 'Editores', 'item': 'Claude'}),
    ('broll-split', 'B-roll dividido', 'B-roll arriba con etiqueta, tú abajo', {'text': 'Gratis'}),
    ('phone-fan', 'Abanico de teléfonos', 'Tus reels en abanico como cartas', {'text': 'Mis videos|editados con Claude'}),
    ('dot-reveal', 'Puntos', 'Tu imagen se arma con puntos brillantes', {}),
    ('headline-wall', 'Muro de titulares', 'Tus titulares se apilan detrás y aparece un total', {'text': 'Corta las pausas::1 clic|Subtítulos solos::Claude|Color de cine::auto', 'total': '3', 'label': 'pasos'}),
    ('checklist', 'Checklist de Claude', 'Lista de tareas de Claude bajo tu barbilla', {'text': 'Cortes::listo|Subtítulos::listo|Zoom::listo', 'title': 'Claude'}),
    ('liquid-glass-graph', 'Gráfica de vidrio', 'Tarjeta de vidrio con gráfica que sube', {'text': 'seguidores', 'from': '0', 'to': '10K'}),
    ('carousel-spin', 'Carrusel 3D', 'Tus reels giran alrededor de ti en 3D', {}),
    ('match-cut', 'Corte de noticias', 'Páginas de noticias que cortan en una palabra', {'text': 'Claude'}),
    ('apple-toggles', 'Interruptores iPhone', 'Interruptores de iPhone que se encienden', {'text': 'Cortes|Subtítulos|Zoom'}),
    ('led-sign', 'Letrero LED', 'Se apagan las luces y un letrero LED se escribe', {'text': 'EDITADO|CON CLAUDE'}),
    ('slow-push', 'Empuje lento', 'Zoom lento de cine con el fondo desenfocado', {}),
    ('over-the-shoulder-zoom', 'Sobre el hombro', 'La cámara va a una esquina y aparece una gráfica', {'text': 'antes|después', 'to': '1:50|0:37'}),
    ('messages', 'Mensajes', 'Notificaciones de iMessage una tras otra', {'text': 'Ya está tu video|Quedó increíble|¿Cómo lo hiciste?', 'title': 'Mensajes'}),
    ('place-in-grid', 'En tu perfil', 'Te encoges al centro de tu perfil de 3x3', {}),
    ('tape-label', 'Cinta', 'Una cinta amarilla con tu frase en el pecho', {'text': 'editado con Claude'}),
    ('select-resize', 'Seleccionar y agrandar', 'Una caja azul agarra tu número y lo agranda', {'text': '2X'}),
    ('wave-trim', 'Recorte de voz', 'Los silencios de tu voz se recortan en pantalla', {}),
    ('huge-strike', 'Palabra tachada', 'Palabra gigante detrás que se tacha', {'text': 'CapCut'}),
    ('crayon-write', 'Crayón', 'Un crayón rojo escribe tu palabra detrás', {'text': 'Claude'}),
    ('fan-build', 'Abanico de portadas', 'Tus portadas se reparten en abanico detrás', {}),
]


def render(e, clip):
    fid, nombre, uso, opts = e
    os.makedirs(os.path.join(SAL, GRUPO[fid]), exist_ok=True)
    out = os.path.join(SAL, GRUPO[fid], f'{fid}.mp4')
    plan = os.path.join(SAL, f'_{fid}.json')
    try: arroba = json.load(open(os.path.join(RAIZ, 'brand.json'))).get('handle') or '@tu_usuario'
    except Exception: arroba = '@tu_usuario'
    opts = {k: (v.replace('@tu_usuario', arroba) if isinstance(v, str) else v) for k, v in opts.items()}
    json.dump({'effects': [dict(opts, fx=fid, start=0.3, end=3.9)]}, open(plan, 'w'), ensure_ascii=False)
    r = subprocess.run([sys.executable, FX, '--plan', plan, clip, out, '--width', '540'], capture_output=True, text=True)
    os.remove(plan)
    return fid, r.returncode, r.stderr[-300:]


def main():
    clip = next((a for a in sys.argv[1:] if not a.startswith('--') and a.endswith('.mp4')), os.path.join(SAL, '_clip.mp4'))
    solo = sys.argv[sys.argv.index('--solo') + 1].split(',') if '--solo' in sys.argv else None
    lista = [e for e in EFECTOS if not solo or e[0] in solo]
    with ThreadPoolExecutor(4) as ex:
        for fid, rc, err in ex.map(lambda e: render(e, clip), lista):
            print('✓' if rc == 0 else '✗', fid, '' if rc == 0 else err, flush=True)
    json.dump({'carpetas': [{'id': c[0], 'nombre': c[1], 'uso': c[2]} for c in CARPETAS],
               'efectos': [{'id': f, 'nombre': n, 'uso': u, 'carpeta': GRUPO[f], 'ejemplo': o} for f, n, u, o in EFECTOS]},
              open(os.path.join(RAIZ, 'banco', 'camara.json'), 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
