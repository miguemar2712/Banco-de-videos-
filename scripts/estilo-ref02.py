#!/usr/bin/env python3
"""Monta un video con el ESTILO REF 02 (ver referencias/ref02-estilo.md).

Uso:  .venv/bin/python scripts/estilo-ref02.py ediciones/<nombre>/ref02.json

ref02.json:
{
  "audio": "videos/x.mov",            # voz (se usa COMPLETA desde 0 hasta "duracion")
  "palabras": "ediciones/x/palabras.json",
  "duracion": 20.5,
  "salida": "out/x.mp4",
  "tomas":  [{"src": "videos/x.mov", "desde": 0, "a": 0, "hasta": 1.9}],   # a = inicio en el video final
  "titulos": [{"de": 0, "a": 1.9, "titular": "EMPEZAR DE CERO", "cursiva": "si hoy me tocara", "y": 1060}],
  "etiquetas": [{"de": 1.9, "a": 3.4, "texto": "ENCUESTA", "x": 760, "y": 560, "rot": -7}],
  "claves": ["encuesta", ...],          # palabras de los subtítulos que crecen
  "ocultar_subs": [[16.0, 20.5]],
  "cta": {"de": 16.0, "titular": "ESCRÍBEME", "cursiva": "\"empezar\""}
}
Capas: video > sombreado local > etiquetas > subtítulos > títulos > dim CTA.
"""
import json, math, os, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = lambda n: os.path.join(RAIZ, 'fuentes', n)
W, H, FPS = 1080, 1920, 30
CREMA, BLANCO, TINTA, ROSA = (255, 240, 175), (255, 255, 255), (23, 24, 23), (246, 140, 191)
TITULAR_F, CURSIVA_F = F('Anton-Regular.ttf'), F('PlayfairDisplayBlackItalic.ttf')
SUB_F, SUB_CLAVE_F = F('Montserrat-ExtraBold.ttf'), F('Montserrat-Black.ttf')
MARGEN = 90
_fc = {}


def font(p, s):
    k = (p, int(s))
    if k not in _fc:
        _fc[k] = ImageFont.truetype(p, int(s))
    return _fc[k]


def ease_out(x):
    x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3


def texto_tracking(txt, f, track):
    """Imagen RGBA del texto con tracking (fracción del tamaño, negativo = más junto)."""
    sp = f.size * track
    anchos = [f.getlength(c) for c in txt]
    w = int(sum(anchos) + sp * (len(txt) - 1) + f.size * 0.4) + 4
    asc, desc = f.getmetrics()
    im = Image.new('L', (max(w, 1), asc + desc + 8), 0)
    d = ImageDraw.Draw(im); x = f.size * 0.2
    for c, a in zip(txt, anchos):
        d.text((x, 4), c, font=f, fill=255); x += a + sp
    bb = im.getbbox() or (0, 0, 1, 1)
    return im.crop(bb)


def pegar_con_sombra(base, mask, color, cx, cy, escala=1.0, alpha=1.0, blur=10, off=(0, 6), sombra=0.55):
    if escala != 1.0:
        mask = mask.resize((max(1, int(mask.width * escala)), max(1, int(mask.height * escala))), Image.LANCZOS)
    x, y = int(cx - mask.width / 2), int(cy - mask.height / 2)
    if sombra > 0:
        pad = blur * 3
        sm = Image.new('L', (mask.width + pad * 2, mask.height + pad * 2), 0)
        sm.paste(mask, (pad, pad)); sm = sm.filter(ImageFilter.GaussianBlur(blur))
        sm = sm.point(lambda v: int(v * sombra * alpha))
        capa = Image.new('RGBA', sm.size, TINTA + (0,)); capa.putalpha(sm)
        base.alpha_composite(capa, (x - pad + off[0], y - pad + off[1]))
    m = mask.point(lambda v: int(v * alpha)) if alpha < 1 else mask
    capa = Image.new('RGBA', mask.size, color + (0,)); capa.putalpha(m)
    base.alpha_composite(capa, (x, y))
    return mask.width, mask.height


def ajustar(txt, fpath, tam, maxw, track=0.0):
    while tam > 20:
        m = texto_tracking(txt, font(fpath, tam), track)
        if m.width <= maxw:
            return m
        tam -= 4
    return texto_tracking(txt, font(fpath, tam), track)


# ------------------------------------------------------------------ capas
def capa_titulo(base, t, ti):
    de, a = ti['de'], ti['a']
    if not (de <= t < a):
        return
    cy = ti.get('y', 1060)
    tam = ti.get('tam', 135)
    m = ajustar(ti['titular'].upper(), TITULAR_F, tam, W - 2 * MARGEN, -0.03)
    k = ease_out((t - de) / (6 / FPS))                     # pop 115 % -> 100 % en 6 frames
    esc = 1.15 - 0.15 * k
    salida = max(0.0, min(1.0, (a - t) / (4 / FPS)))
    pegar_con_sombra(base, m, CREMA, W / 2, cy, esc, alpha=min(1.0, k * 1.5) * salida, blur=12)
    if ti.get('cursiva'):
        kc = ease_out((t - de - 3 / FPS) / (8 / FPS))      # fade + subida en 8 frames, entra 3 frames después
        mc = ajustar(ti['cursiva'], CURSIVA_F, ti.get('tam_cursiva', 86), W - 2 * MARGEN - 60)
        cyc = cy + m.height / 2 + mc.height * 0.42 + 24 * (1 - kc)   # solapada con el titular
        pegar_con_sombra(base, mc, BLANCO, W / 2 + ti.get('dx_cursiva', 40), cyc, 1.0, alpha=kc * salida, blur=8, sombra=0.6)


def capa_etiqueta(base, t, e):
    de, a = e['de'], e['a']
    if not (de <= t < a):
        return
    k = (t - de) * FPS
    # pop + microrebote: 0.6 -> 1.08 -> 0.97 -> 1.0
    if k < 5: esc = 0.6 + 0.48 * ease_out(k / 5)
    elif k < 9: esc = 1.08 - 0.11 * ((k - 5) / 4)
    elif k < 12: esc = 0.97 + 0.03 * ((k - 9) / 3)
    else: esc = 1.0
    balanceo = math.sin((t - de) * 2.4) * 1.5
    salida = max(0.0, min(1.0, (a - t) / (3 / FPS)))
    f = font(SUB_CLAVE_F, e.get('tam', 64))
    m = texto_tracking(e['texto'], f, -0.01)
    tw, th = m.width + 70, m.height + 64
    S = 2
    eti = Image.new('RGBA', ((tw + 40) * S, (th + 150) * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(eti)
    ox, oy = 20 * S, 130 * S
    # cuerda
    d.line([(ox + tw * S // 2, 0), (ox + tw * S // 2, oy + 26 * S)], fill=(245, 245, 240, 255), width=3 * S)
    # etiqueta con esquina cortada arriba + ojal
    c = 26 * S
    poly = [(ox + c, oy), (ox + tw * S - c, oy), (ox + tw * S, oy + c), (ox + tw * S, oy + th * S),
            (ox, oy + th * S), (ox, oy + c)]
    d.polygon(poly, fill=ROSA + (255,))
    d.ellipse([ox + tw * S // 2 - 9 * S, oy + 14 * S, ox + tw * S // 2 + 9 * S, oy + 32 * S], fill=(250, 250, 245, 255))
    mm = m.resize((m.width * S, m.height * S), Image.LANCZOS)
    blanco = Image.new('RGBA', mm.size, BLANCO + (0,)); blanco.putalpha(mm)
    eti.alpha_composite(blanco, (ox + (tw * S - mm.width) // 2, oy + 44 * S))
    eti = eti.resize((eti.width // S, eti.height // S), Image.LANCZOS)
    eti = eti.resize((max(1, int(eti.width * esc)), max(1, int(eti.height * esc))), Image.LANCZOS)
    eti = eti.rotate(e.get('rot', -6) + balanceo, resample=Image.BICUBIC, expand=True,
                     center=(eti.width / 2, 0))
    if salida < 1:
        eti.putalpha(eti.getchannel('A').point(lambda v: int(v * salida)))
    # sombra suave
    sh = Image.new('RGBA', eti.size, TINTA + (0,)); sh.putalpha(eti.getchannel('A').filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * .45)))
    x, y = int(e['x'] - eti.width / 2), int(e['y'] - 130 * esc)
    base.alpha_composite(sh, (x + 6, y + 10)); base.alpha_composite(eti, (x, y))


def grupos_subs(palabras, dur):
    """Grupitos de 1-3 palabras que cambian con la voz."""
    g, act = [], []
    for i, w in enumerate(palabras):
        act.append(w)
        fin_frase = re.search(r'[.,!?]$', w['text'])
        sig = palabras[i + 1] if i + 1 < len(palabras) else None
        hueco = sig and sig['start'] - w['end'] > 0.25
        if len(act) >= 3 or fin_frase or hueco or not sig:
            g.append(act); act = []
    out = []
    for i, grp in enumerate(g):
        de = grp[0]['start']
        a = g[i + 1][0]['start'] if i + 1 < len(g) else min(dur, grp[-1]['end'] + 0.4)
        a = min(a, grp[-1]['end'] + 0.6)
        out.append((de, a, grp))
    return out


def limpiar(w):
    return re.sub(r'[.,!?¿¡]', '', w)


def capa_subs(base, t, grupos, claves, cy):
    for de, a, grp in grupos:
        if not (de <= t < a):
            continue
        piezas = []
        for w in grp:
            if w['start'] > t:
                break
            clave = limpiar(w['text']).lower() in claves
            fp, tam = (SUB_CLAVE_F, 92) if clave else (SUB_F, 60)
            k = ease_out((t - w['start']) / (4 / FPS))
            piezas.append((limpiar(w['text']).upper() if clave else limpiar(w['text']), fp, tam, k, clave))
        if not piezas:
            return
        masks = [(texto_tracking(p[0], font(p[1], p[2]), 0.0), p) for p in piezas]
        esp = 22
        total = sum(m.width for m, _ in masks) + esp * (len(masks) - 1)
        if total > W - 2 * MARGEN:                              # reducir si no cabe
            f = (W - 2 * MARGEN) / total
            masks = [(m.resize((int(m.width * f), int(m.height * f)), Image.LANCZOS), p) for m, p in masks]
            total = sum(m.width for m, _ in masks) + esp * (len(masks) - 1)
        x = W / 2 - total / 2
        for m, p in masks:
            esc = 1.12 - 0.12 * p[3]
            pegar_con_sombra(base, m, CREMA if p[4] else BLANCO, x + m.width / 2, cy - (m.height - 44) * 0.0,
                             esc, alpha=p[3], blur=9, off=(0, 4), sombra=0.6)
            x += m.width + esp
        return


def capa_cta(base, t, cta, dur):
    de = cta['de']
    if t < de:
        return
    k = ease_out((t - de) / 0.8)
    dim = Image.new('RGBA', (W, H), TINTA + (int(255 * 0.62 * k),))   # oscurecer 62 %
    base.alpha_composite(dim)
    capa_titulo(base, t, {'de': de + 0.15, 'a': dur + 1, 'titular': cta['titular'], 'cursiva': cta.get('cursiva'),
                          'y': cta.get('y', 900), 'tam': 150, 'tam_cursiva': 92, 'dx_cursiva': 30})


def sombreado_local(base, cy, alto=520):
    """Degradado oscuro suave detrás de títulos/subtítulos para que se lean."""
    g = Image.new('L', (1, alto))
    for i in range(alto):
        g.putpixel((0, i), int(110 * math.sin(math.pi * i / alto) ** 1.5))
    capa = Image.new('RGBA', (W, alto), TINTA + (0,)); capa.putalpha(g.resize((W, alto)))
    base.alpha_composite(capa, (0, int(cy - alto / 2)))


# ------------------------------------------------------------------ video base
def base_video(cfg, tmp):
    partes = []
    for i, tm in enumerate(cfg['tomas']):
        dur = tm['hasta'] - tm['a']
        z0, z1 = tm.get('zoom', [1.04, 1.08])
        out = os.path.join(tmp, f'p{i:02d}.mp4')
        vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
              f"scale=w='trunc({W}*({z0}+({z1}-{z0})*t/{dur})/2)*2':h=-2:eval=frame,crop={W}:{H},"
              f"fps={FPS},setsar=1,format=yuv420p")
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(tm['desde']), '-t', f'{dur:.3f}', '-i', tm['src'],
                        '-an', '-vf', vf, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '12', out], check=True)
        partes.append(out)
    lista = os.path.join(tmp, 'lista.txt')
    open(lista, 'w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in partes))
    base = os.path.join(tmp, 'base.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lista, '-c', 'copy', base], check=True)
    return base


def main():
    cfg = json.load(open(sys.argv[1]))
    borrador = '--borrador' in sys.argv
    dur = cfg['duracion']
    tmp = os.path.join(os.path.dirname(sys.argv[1]), '_tmp'); os.makedirs(tmp, exist_ok=True)
    base = base_video(cfg, tmp)
    pal = json.load(open(cfg['palabras']))['words']
    for r in cfg.get('reemplazos', []):
        for w in pal:
            if limpiar(w['text']).lower() == r[0].lower():
                w['text'] = w['text'].replace(limpiar(w['text']), r[1])
    grupos = grupos_subs(pal, dur)
    claves = {c.lower() for c in cfg.get('claves', [])}
    ocultar = cfg.get('ocultar_subs', [])
    subs_y = cfg.get('subs_y', 1420)
    salida = cfg['salida']; os.makedirs(os.path.dirname(salida), exist_ok=True)
    cmd = ['ffmpeg', '-v', 'error', '-y', '-i', base,
           '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-i', cfg['audio'],
           '-filter_complex', '[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v]',
           '-map', '[v]', '-map', '2:a', '-t', str(dur),
           '-c:v', 'libx264', '-preset', 'medium' if not borrador else 'veryfast', '-crf', '18',
           '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', salida]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = int(round(dur * FPS))
    for i in range(n):
        t = i / FPS
        im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        hay_sub = not any(a <= t < b for a, b in ocultar) and any(de <= t < a for de, a, _ in grupos)
        hay_tit = any(ti['de'] <= t < ti['a'] for ti in cfg.get('titulos', []))
        if hay_sub: sombreado_local(im, subs_y, 300)
        for ti in cfg.get('titulos', []):
            if ti['de'] <= t < ti['a']: sombreado_local(im, ti.get('y', 1060) + 40, 520)
        for e in cfg.get('etiquetas', []): capa_etiqueta(im, t, e)
        if hay_sub: capa_subs(im, t, grupos, claves, subs_y)
        for ti in cfg.get('titulos', []): capa_titulo(im, t, ti)
        if cfg.get('cta'): capa_cta(im, t, cfg['cta'], dur)
        p.stdin.write(im.tobytes())
    p.stdin.close(); p.wait()
    print('✓', salida)


if __name__ == '__main__':
    main()
