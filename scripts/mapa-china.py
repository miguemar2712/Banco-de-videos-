#!/usr/bin/env python3
"""Dibuja assets/china-mapa.png: silueta de China en rojo con estrellas amarillas (contorno: Natural Earth, dominio público)."""
import json, math, os
from PIL import Image, ImageDraw, ImageFilter
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
g = json.load(open(os.path.join(RAIZ, 'assets', 'china.geojson')))['geometry']['coordinates']
W, ESC = 680, 4  # ancho final, supermuestreo
k = math.cos(math.radians(34))
pts = [(lon * k, -lat) for poly in g for ring in poly for lon, lat in ring]
x0, x1 = min(p[0] for p in pts), max(p[0] for p in pts); y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)
s = (W * ESC - 40 * ESC) / (x1 - x0); H = int((y1 - y0) * s / ESC) + 40
im = Image.new('RGBA', (W * ESC, H * ESC), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
P = lambda lon, lat: ((lon * k - x0) * s + 20 * ESC, (-lat - y0) * s + 20 * ESC)
for poly in g:
    if len(poly[0]) < 8: continue          # sin islitas diminutas
    d.polygon([P(*c) for c in poly[0]], fill=(222, 32, 30, 255))
def estrella(cx, cy, r, rot=0):
    v = []
    for i in range(10):
        a = math.radians(-90 + rot + i * 36); rr = r if i % 2 == 0 else r * .38
        v.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(v, fill=(255, 222, 0, 255))
cx, cy = P(92, 36); R = 46 * ESC                               # estrella grande sobre el centro-oeste
estrella(cx, cy, R)
for dx, dy, rot in ((1.9, -1.3, 20), (2.5, -.5, 45), (2.5, .5, 0), (1.9, 1.2, 20)):
    estrella(cx + dx * R, cy + dy * R, R * .34, rot)
im = im.resize((W, H), Image.LANCZOS)
sombra = Image.new('RGBA', im.size, (0, 0, 0, 0)); sombra.putalpha(im.getchannel('A').point(lambda a: a * .35))
sombra = sombra.filter(ImageFilter.GaussianBlur(6))
out = Image.new('RGBA', im.size, (0, 0, 0, 0)); out.alpha_composite(sombra, (0, 4)); out.alpha_composite(im)
out.save(os.path.join(RAIZ, 'assets', 'china-mapa.png')); print('✓ assets/china-mapa.png', out.size)
