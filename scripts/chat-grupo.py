#!/usr/bin/env python3
"""Animación vertical (1080x1920) de un celular con un GRUPO abierto donde llegan muchos mensajes seguidos.
Para cuando ella dice "comunidad". Mensajes neutros (saludos y fotos de su mercancía), nunca reseñas inventadas.

uso: .venv/bin/python scripts/chat-grupo.py salida.mp4 --nombre "Comunidad" --sub "3,000+ miembros" --dur 3.0
        [--fondo videos/clip-d.mov] [--fotos videos/clip-c.mov,videos/clip-d.mov] [--privado] [--semilla 1]
"""
import argparse, os, random, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFilter, ImageFont

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
F = os.path.join(RAIZ, 'fx-camara', 'fonts')
ap = argparse.ArgumentParser()
ap.add_argument('salida'); ap.add_argument('--nombre', default='Comunidad'); ap.add_argument('--sub', default='')
ap.add_argument('--dur', type=float, default=3.0); ap.add_argument('--fondo'); ap.add_argument('--fotos', default='')
ap.add_argument('--privado', action='store_true'); ap.add_argument('--pedido', action='store_true'); ap.add_argument('--semilla', type=int, default=1)
a = ap.parse_args()
rnd = random.Random(a.semilla)
W, H, FPS = 1080, 1920, 30
N = int(a.dur * FPS)


def frame_de(video, t):
    f = tempfile.mktemp(suffix='.png')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', video, '-frames:v', '1', f], check=True)
    im = Image.open(f).convert('RGB'); os.remove(f); return im


def llenar(im, w, h):
    r = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


# fondo: su mercancía desenfocada y oscurecida
fondo = llenar(frame_de(a.fondo, 1.0), W, H).filter(ImageFilter.GaussianBlur(28)) if a.fondo else Image.new('RGB', (W, H), (40, 30, 30))
fondo = Image.blend(fondo, Image.new('RGB', (W, H), (0, 0, 0)), .35)
fotos = []
for i, v in enumerate([x for x in a.fotos.split(',') if x]):
    for t in (1.0, 3.0, 5.0):
        try: fotos.append(llenar(frame_de(v, t), 300, 300))
        except Exception: pass

# teléfono
PW, PH = 680, 1250; PX, PY = (W - PW) // 2, 650   # debajo del título y el mapa
fnt = lambda s, b=False: ImageFont.truetype(os.path.join(F, 'Inter.ttf'), s)
NOMBRES = ['Ana', 'Karla', 'Mayra', 'Luz', 'Sofi', 'Dani', 'Yesi', 'Caro', 'Vane', 'Paty', 'Gaby', 'Rosa', 'Lili', 'Fer', 'Mari', 'Jess']
TEXTOS = ['Hola a todas', 'Buenos días', 'Hola!', 'Holaa', 'Saludos desde aquí', 'Presente', 'Buenas noches', 'Hola chicas',
          'Aquí estoy', 'Gracias por agregarme', 'Hola, soy nueva', 'Bienvenidas', 'Hola grupo', 'Buen día a todas']
COLORES = [(230, 90, 120), (90, 150, 230), (240, 150, 60), (120, 190, 100), (170, 110, 220), (60, 180, 180), (220, 80, 80)]
msgs = []
t = 0.15
while t < a.dur + .3:
    foto = fotos and rnd.random() < .22
    msgs.append(dict(t=t, n=rnd.choice(NOMBRES), c=rnd.choice(COLORES), txt=None if foto else rnd.choice(TEXTOS),
                     foto=rnd.choice(fotos) if foto else None))
    t += rnd.uniform(.11, .22)
if a.pedido:   # chat 1 a 1 con su proveedor: ella pide, el proveedor manda fotos y confirma
    guion = [(0.15, True, 'Hola, quiero hacer un pedido', None), (0.55, False, None, 0), (0.8, False, None, 1),
             (1.1, False, 'Estos son los modelos', None), (1.5, True, 'Me llevo estos', None), (1.9, False, None, 2),
             (2.25, False, 'Perfecto, lo empacamos hoy', None), (2.6, True, 'Gracias!', None)]
    k = a.dur / 2.9
    msgs = [dict(t=t * k, yo=yo, n='Proveedor', c=(18, 140, 120), txt=txt, foto=(fotos[f % len(fotos)] if f is not None and fotos else None))
            for t, yo, txt, f in guion if (txt or (f is not None and fotos))]
for m in msgs:
    m.setdefault('yo', False)
    m['h'] = (360 if m['foto'] else 118) - (40 if m['yo'] or a.pedido else 0)


def burbuja(m):
    w = 340 if m['foto'] else min(560, 60 + int(fnt(36).getlength(m['txt'])) + 40)
    w = max(w, 60 + int(fnt(28).getlength(m['n'])) + 30)
    b = Image.new('RGBA', (w, m['h'] - 14), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.rounded_rectangle((0, 0, w - 1, m['h'] - 15), 26, fill=(217, 253, 211, 255) if m['yo'] else (255, 255, 255, 255))
    top = 18
    if not (m['yo'] or a.pedido):
        d.text((26, 14), '~ ' + m['n'], font=fnt(28), fill=m['c']); top = 58
    if m['foto']:
        b.paste(m['foto'].resize((w - 40, m['h'] - top - 22)), (20, top))
    else:
        d.text((26, top - 6), m['txt'], font=fnt(36), fill=(30, 30, 30))
    return b


cache = {}
tmp = tempfile.mkdtemp()
for k in range(N):
    tt = k / FPS
    im = fondo.copy().convert('RGBA')
    tel = Image.new('RGBA', (PW, PH), (0, 0, 0, 0)); d = ImageDraw.Draw(tel)
    d.rounded_rectangle((0, 0, PW - 1, PH - 1), 70, fill=(20, 20, 22, 255))
    pant = Image.new('RGBA', (PW - 36, PH - 36), (236, 229, 221, 255)); dp = ImageDraw.Draw(pant)
    # mensajes visibles (los nuevos entran abajo y empujan hacia arriba)
    vis = [m for m in msgs if m['t'] <= tt]
    y = pant.height - 120
    for m in reversed(vis):
        anim = min(1, (tt - m['t']) / .12)
        y -= int(m['h'] * anim)
        if y < 150: break
        b = cache.setdefault(id(m), burbuja(m))
        pant.alpha_composite(b, (pant.width - b.width - 28 if m['yo'] else 28, max(150, y)))
    # barra de arriba (nombre del grupo)
    dp.rectangle((0, 0, pant.width, 150), fill=(18, 110, 96, 255))
    dp.ellipse((90, 30, 180, 120), fill=(230, 60, 60, 255))
    dp.text((135, 75), 'P' if a.pedido else 'DC', font=fnt(34), fill='white', anchor='mm')
    dp.text((200, 34), a.nombre + ('  🔒' if False else ''), font=fnt(40), fill='white')
    if a.privado:
        dp.rounded_rectangle((200 + fnt(40).getlength(a.nombre) + 16, 40, 200 + fnt(40).getlength(a.nombre) + 136, 82), 12, fill=(255, 255, 255, 60))
        dp.text((200 + fnt(40).getlength(a.nombre) + 76, 61), 'privado', font=fnt(24), fill='white', anchor='mm')
    sub = a.sub if int(tt * 4) % 2 or tt < .6 else 'escribiendo…'
    dp.text((200, 88), sub, font=fnt(28), fill=(220, 240, 235))
    dp.text((40, 72), '‹', font=fnt(60), fill='white', anchor='mm')
    # barra de escribir
    dp.rectangle((0, pant.height - 100, pant.width, pant.height), fill=(240, 240, 240, 255))
    dp.rounded_rectangle((24, pant.height - 82, pant.width - 120, pant.height - 20), 30, fill='white')
    dp.text((60, pant.height - 51), 'Mensaje', font=fnt(30), fill=(150, 150, 150), anchor='lm')
    dp.ellipse((pant.width - 100, pant.height - 88, pant.width - 24, pant.height - 12), fill=(18, 140, 120, 255))
    # contador de mensajes nuevos
    nuevos = len(vis)
    if nuevos and not a.pedido:
        dp.rounded_rectangle((pant.width - 130, 170, pant.width - 24, 218), 24, fill=(37, 211, 102, 255))
        dp.text((pant.width - 77, 194), f'+{nuevos}', font=fnt(28), fill='white', anchor='mm')
    m = Image.new('L', pant.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, pant.width - 1, pant.height - 1), 56, fill=255)
    tel.paste(pant, (18, 18), m)
    sombra = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sombra).rounded_rectangle((PX + 10, PY + 30, PX + PW + 10, PY + PH + 30), 70, fill=(0, 0, 0, 140))
    im.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(30)))
    esc = 1 + .04 * min(1, tt / a.dur)                 # acercamiento suave
    tel2 = tel.resize((int(PW * esc), int(PH * esc)), Image.LANCZOS)
    im.alpha_composite(tel2, ((W - tel2.width) // 2, PY - (tel2.height - PH) // 2))
    im.convert('RGB').save(os.path.join(tmp, f'{k:04d}.png'))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', os.path.join(tmp, '%04d.png'), '-c:v', 'libx264',
                '-crf', '16', '-pix_fmt', 'yuv420p', a.salida], check=True)
print('✓', a.salida)
