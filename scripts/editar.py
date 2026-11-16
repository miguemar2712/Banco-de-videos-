#!/usr/bin/env python3
"""Level Up · edita un video completo con HyperFrames a partir de un plan.

Uso:
  python3 scripts/editar.py ediciones/<nombre>/plan.json [--borrador] [--solo-base]

El plan (JSON) usa tiempos del VIDEO ORIGINAL (los de palabras.json); el script los pasa
al video ya cortado. Pasos:
  1. Toma los tramos buenos (quita tomas falladas) y corta silencios > 0,3 s dentro de cada tramo.
  2. HyperFrames → base.mp4  (tu video cortado + zooms + marca Level Up)
  3. HyperFrames → subtitulos.webm (transparente, con el estilo elegido)
  4. HyperFrames → cada motion graphic del banco como .webm transparente con sus textos
  5. Recorte de persona para los efectos "detrás de mí"
  6. ffmpeg une todo + sonidos → out/<nombre>.mp4
"""
import hashlib
import html
import json
import os
import re
import subprocess
import sys

CTA_MOTION = {'ci09', 'ed10', 'cr09'}          # cierres: comenta / sígueme → aquí sale el logo Level Up
CTA_FX = {'comment-box', 'tap', 'reel-frame'}
BAJO_BARBILLA = {'checklist', 'liquid-glass-graph', 'tape-label', 'apple-toggles'}   # efectos de cámara que ocupan la zona de subtítulos
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BANCO = os.path.join(RAIZ, 'banco')
SONIDOS = os.path.join(BANCO, 'assets', 'sonidos')
FPS = 30


def sh(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        print(r.stdout[-3000:], r.stderr[-3000:])
        raise SystemExit(f'Falló: {cmd[:4]}')
    return r.stdout


def duracion(p):
    return float(sh(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]).strip())


# ---------------------------------------------------------------- 1. tramos y palabras
def tokens(t):
    return [x for x in re.split(r'\s+', t.strip()) if x]


def preparar_palabras(plan, palabras):
    """Devuelve (piezas, palabras_cortadas). piezas = [(ini, fin)] en tiempo original."""
    piezas, salida = [], []
    for tr in plan['tramos']:
        ini, fin = tr['de'], tr['a']
        orig = [w for w in palabras if ini - 0.05 <= w['start'] <= fin + 0.05]  # 'a' = inicio de la última palabra del tramo
        texto = tr.get('texto')
        rep = plan.get('reemplazos', {})
        def corrige(t):
            base = t.strip('.,¿?¡!')
            return t.replace(base, rep[base]) if base in rep else t
        toks = tokens(texto) if texto else [corrige(w['text']) for w in orig]
        if not orig:
            raise SystemExit(f'Tramo sin palabras: {ini}-{fin}')
        if len(toks) == len(orig):
            ws = [dict(text=t, start=o['start'], end=o['end']) for t, o in zip(toks, orig)]
        else:  # reparte el tiempo por número de letras
            a, b = orig[0]['start'], orig[-1]['end']
            total = sum(len(t) + 1 for t in toks)
            ws, acc = [], a
            for t in toks:
                d = (b - a) * (len(t) + 1) / total
                ws.append(dict(text=t, start=round(acc, 3), end=round(acc + d * .9, 3)))
                acc += d
        # corta silencios dentro del tramo (salvo pausas que se quieran mantener)
        mantener = tr.get('mantener_pausas', [])
        grupo = [ws[0]]
        for w in ws[1:]:
            hueco = w['start'] - grupo[-1]['end']
            pausa_ok = any(p[0] <= grupo[-1]['end'] + .05 and w['start'] <= p[1] + .05 for p in mantener)
            if hueco > plan.get('silencio', 0.3) and not pausa_ok:
                piezas.append((max(ini - .08, grupo[0]['start'] - .08), grupo[-1]['end'] + .2, grupo))
                grupo = [w]
            else:
                grupo.append(w)
        piezas.append((max(ini - .08, grupo[0]['start'] - .08), grupo[-1]['end'] + .22, grupo))
    if plan.get('cola'):
        a, b, g = piezas[-1]; piezas[-1] = (a, b + plan['cola'], g)
    # mapa original → cortado
    t, mapa = 0.0, []
    for a, b, grupo in piezas:
        mapa.append((a, b, t))
        for w in grupo:
            salida.append(dict(text=w['text'], start=round(w['start'] - a + t, 3), end=round(w['end'] - a + t, 3)))
        t += b - a
    return [(a, b) for a, b, _ in piezas], mapa, salida, t


def a_cortado(mapa, x):
    for a, b, t in mapa:
        if a - 0.01 <= x <= b + 0.01:
            return round(t + (x - a), 3)
    # si cae en un hueco, va al inicio de la siguiente pieza
    for a, b, t in mapa:
        if x < a:
            return round(t, 3)
    a, b, t = mapa[-1]
    return round(t + (b - a), 3)


def cortar_video(src, piezas, out):
    f, cats = [], []
    for i, (a, b) in enumerate(piezas):
        d = b - a
        f.append(f'[0:v]trim=start={a:.3f}:end={b:.3f},setpts=PTS-STARTPTS[v{i}]')
        f.append(f'[0:a]atrim=start={a:.3f}:end={b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={max(0, d - 0.02):.3f}:d=0.02[a{i}]')
        cats.append(f'[v{i}][a{i}]')
    f.append(''.join(cats) + f'concat=n={len(piezas)}:v=1:a=1[v][a]')
    sh(['ffmpeg', '-v', 'error', '-y', '-i', src, '-filter_complex', ';'.join(f), '-map', '[v]', '-map', '[a]',
        '-c:v', 'libx264', '-crf', '17', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709',
        '-color_trc', 'bt709', '-colorspace', 'bt709', '-c:a', 'aac', '-b:a', '192k', out])


# ---------------------------------------------------------------- 2a. base con ffmpeg (calidad máxima)
def expr_zoom(zooms):
    """Devuelve (expresión de escala Z(t), expresión de sacudida en x) para ffmpeg."""
    partes, sac = [], []
    for z in zooms:
        a, d, s = z['t'], z.get('dur', 1.2), z.get('escala', 1.18)
        tipo = z.get('tipo', 'golpe')
        if tipo == 'golpe':
            partes.append(f"if(between(t,{a:.3f},{a + .14:.3f}),({s - 1:.4f})*(1-pow(1-(t-{a:.3f})/0.14,3)),0)")
            partes.append(f"if(between(t,{a + .14:.3f},{a + d:.3f}),{s - 1:.4f},0)")
            partes.append(f"if(between(t,{a + d:.3f},{a + d + .3:.3f}),({s - 1:.4f})*(0.5+0.5*cos(PI*(t-{a + d:.3f})/0.3)),0)")
        elif tipo == 'suave':
            partes.append(f"if(between(t,{a:.3f},{a + d:.3f}),({s - 1:.4f})*(0.5-0.5*cos(PI*(t-{a:.3f})/{d:.3f})),0)")
            partes.append(f"if(between(t,{a + d:.3f},{a + d + .4:.3f}),({s - 1:.4f})*(0.5+0.5*cos(PI*(t-{a + d:.3f})/0.4)),0)")
        elif tipo == 'sacudida':
            partes.append(f"if(between(t,{a:.3f},{a + .45:.3f}),0.05,0)")
            sac.append(f"if(between(t,{a:.3f},{a + .42:.3f}),18*sin(2*PI*22*(t-{a:.3f})),0)")
    Z = '1+' + '+'.join(partes) if partes else '1'
    X = '+'.join(sac) if sac else '0'
    return Z, X


def base_ffmpeg(src, piezas, zooms, out, color=True):
    f, cats = [], []
    for i, (a, b) in enumerate(piezas):
        d = b - a
        f.append(f'[0:v]trim=start={a:.3f}:end={b:.3f},setpts=PTS-STARTPTS[v{i}]')
        f.append(f'[0:a]atrim=start={a:.3f}:end={b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={max(0, d - 0.025):.3f}:d=0.025[a{i}]')
        cats.append(f'[v{i}][a{i}]')
    f.append(''.join(cats) + f'concat=n={len(piezas)}:v=1:a=1[vc][a]')
    Z, X = expr_zoom(zooms)
    it = lambda e: re.sub(r'\bt\b', 'it', e)   # zoompan usa "it" = tiempo del cuadro de entrada
    # zoom por cuadro con zoompan (crop+scale con tamaño variable no se recalcula y recortaba desde la esquina)
    cadena = (f"[vc]fps=30,zoompan=z='{it(Z)}':x='(iw-iw/zoom)/2+({it(X)})/zoom':y='(ih-ih/zoom)*0.38':d=1:s=1080x1920:fps=30")
    for z in zooms:
        if z.get('tipo') == 'byn':
            cadena += f",hue=s=0:enable='between(t,{z['t']:.3f},{z['t'] + z.get('dur', 1.2):.3f})'"
    if color:  # corrección suave: algo de contraste y color natural (nunca amarillento) + nitidez
        cadena += ",eq=contrast=1.04:saturation=1.05:gamma=0.99,unsharp=5:5:0.45:5:5:0.0"
    grades = [z for z in zooms if z.get('tipo') == 'grade']
    if not grades:
        f.append(cadena + ',format=yuv420p[v]')
    else:
        # ColorGrade: 0–25 cuadros plano, 25–45 barrido con línea de luz (capa cl06), luego cinematográfico
        f.append(cadena + f',format=yuv420p,split={1 + 2 * len(grades)}' + ''.join(f'[g{i}]' for i in range(1 + 2 * len(grades))))
        actual = '[g0]'
        for i, z in enumerate(grades):
            a, d = z['t'], z.get('dur', 3.0)
            w0 = a + 25 / 30
            f.append(f'[g{2 * i + 1}]eq=contrast=0.74:saturation=0.6:brightness=0.03[plano{i}]')
            f.append(f'[g{2 * i + 2}]eq=contrast=1.12:saturation=1.08:brightness=-0.01,colorbalance=rs=-0.04:bs=0.05:rh=0.05:gh=0.015:bh=-0.035,vignette=PI/5[cine{i}]')
            f.append(f"[plano{i}][cine{i}]blend=all_expr='if(lt(X,W*clip((T-{w0:.3f})/{20 / 30:.4f},0,1)),B,A)'[mezcla{i}]")
            f.append(f"{actual}[mezcla{i}]overlay=0:0:enable='between(t,{a:.3f},{a + d:.3f})'[gr{i}]")
            actual = f'[gr{i}]'
        f.append(f'{actual}format=yuv420p[v]')
    sh(['ffmpeg', '-v', 'error', '-y', '-i', src, '-filter_complex', ';'.join(f), '-map', '[v]', '-map', '[a]',
        '-c:v', 'libx264', '-crf', '12', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709',
        '-color_trc', 'bt709', '-colorspace', 'bt709', '-c:a', 'aac', '-b:a', '256k', out])


# ---------------------------------------------------------------- 2b. composición base en HyperFrames (solo para marco / pantalla dividida)
BASE_HTML = '''<!doctype html>
<html lang="es"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1080px; height:1920px; overflow:hidden; background:#000; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; }}
#cam {{ position:absolute; inset:0; transform-origin:50% 38%; overflow:hidden; }}
#cam video {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }}
#luz {{ position:absolute; inset:0; pointer-events:none; opacity:0; background:radial-gradient(70% 50% at 50% 30%, rgba(255,236,200,.55), transparent 70%); mix-blend-mode:screen; }}
#flash {{ position:absolute; inset:0; background:#fff; opacity:0; }}
.hojita {{ position:absolute; background-color:{papel}; background-image:linear-gradient(rgba(58,42,31,.07) 1px, transparent 1px), linear-gradient(90deg, rgba(58,42,31,.07) 1px, transparent 1px); background-size:54px 54px; }}
#fondo-marco {{ inset:0; opacity:0; }}
#panel {{ left:0; right:0; top:0; height:960px; opacity:0; box-shadow:0 10px 30px rgba(0,0,0,.25); }}
#marca {{ position:absolute; left:50%; top:1500px; width:132px; margin-left:-66px; opacity:.95; filter:drop-shadow(0 2px 6px rgba(0,0,0,.45)); }}
</style></head><body>
<div id="root" data-composition-id="base" data-start="0" data-duration="{dur:.3f}" data-width="1080" data-height="1920">
  <div id="fondo-marco" class="hojita"></div>
  <div id="cam"><video id="cam-video" src="media/cortado.mp4" data-start="0" data-duration="{dur:.3f}" data-has-audio="true" playsinline></video></div>
  <div id="panel" class="hojita"></div>
  <div id="luz"></div>
  <div id="flash"></div>
  {marca}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{anim}
tl.set({{}}, {{}}, {dur:.3f});
window.__timelines = window.__timelines || {{}};
window.__timelines["base"] = tl;
</script></body></html>'''


def anim_zooms(zooms):
    js = []
    for z in zooms:
        t, d, s = z['t'], z.get('dur', 1.2), z.get('escala', 1.18)
        if z.get('tipo', 'golpe') == 'golpe':
            js.append(f"tl.fromTo('#cam',{{scale:1}},{{scale:{s},duration:.14,ease:'power4.out'}},{t:.3f}).to('#cam',{{scale:1,duration:.3,ease:'power2.inOut'}},{t + d:.3f});")
        elif z['tipo'] == 'suave':
            js.append(f"tl.fromTo('#cam',{{scale:1}},{{scale:{s},duration:{d:.3f},ease:'sine.inOut'}},{t:.3f}).to('#cam',{{scale:1,duration:.4,ease:'power2.inOut'}},{t + d:.3f});")
        elif z['tipo'] == 'sacudida':
            js.append(f"tl.to('#cam',{{x:18,rotation:.6,duration:.05,yoyo:true,repeat:7,ease:'none'}},{t:.3f}).set('#cam',{{x:0,rotation:0}},{t + .42:.3f});")
        elif z['tipo'] == 'flash':
            js.append(f"tl.fromTo('#flash',{{opacity:.9}},{{opacity:0,duration:.35,ease:'power2.out',immediateRender:false}},{t:.3f});")
        elif z['tipo'] == 'luz':
            js.append(f"tl.fromTo('#luz',{{opacity:0}},{{opacity:1,duration:.5,immediateRender:false}},{t:.3f}).to('#luz',{{opacity:0,duration:.6}},{t + d:.3f});")
        elif z['tipo'] == 'dividida':
            js.append(f"tl.set('#panel',{{opacity:1}},{t:.3f}).set('#cam',{{y:{z.get('bajar', 620)}}},{t:.3f}).set('#panel',{{opacity:0}},{t + d:.3f}).set('#cam',{{y:0}},{t + d:.3f});")
        elif z['tipo'] == 'marco':
            js.append(f"tl.set('#fondo-marco',{{opacity:1}},{t:.3f}).to('#cam',{{scale:{z.get('escala', .74)},borderRadius:46,boxShadow:'0 0 0 12px #fff, 0 40px 80px rgba(0,0,0,.35)',duration:.45,ease:'power3.inOut'}},{t:.3f}).to('#cam',{{scale:1,borderRadius:0,boxShadow:'0 0 0 0px #fff, 0 0 0 rgba(0,0,0,0)',duration:.4,ease:'power3.inOut'}},{t + d:.3f}).set('#fondo-marco',{{opacity:0}},{t + d + .4:.3f});")
        elif z['tipo'] == 'byn':
            js.append(f"tl.set('#cam',{{filter:'grayscale(1) contrast(1.1)'}},{t:.3f}).set('#cam',{{filter:'none'}},{t + d:.3f});")
    return '\n'.join(js)


# ---------------------------------------------------------------- 3. subtítulos por estilo
SUB_CSS = {
    'impacto': '''
.g { position:absolute; left:120px; right:120px; top:928px; text-align:center; opacity:0; }
.g span { font-family:'Anton',Impact,sans-serif; font-size:118px; line-height:1; letter-spacing:1px; text-transform:uppercase; color:#fff;
  text-shadow:0 6px 0 rgba(0,0,0,.35), 0 10px 30px rgba(0,0,0,.55); }
.g.clave span { color:var(--acento); font-size:132px; }''',
    'editorial': '''
.g { position:absolute; left:120px; right:120px; top:948px; text-align:center; opacity:0; }
.g span { font-family:'Poppins',sans-serif; font-weight:700; font-size:76px; line-height:1.05; color:#fff; letter-spacing:-1px;
  text-shadow:0 3px 14px rgba(40,25,10,.55); }
.g span.k { font-family:'Playfair Display',serif; font-style:italic; font-weight:600; font-size:96px; color:var(--acento2); letter-spacing:0; }''',
    'cinematico': '''
.g { position:absolute; left:120px; right:120px; top:955px; text-align:center; opacity:0; }
.g span { font-family:'Inter',sans-serif; font-weight:700; font-size:68px; color:#F7F1E8; letter-spacing:-1.5px;
  text-shadow:0 4px 24px rgba(0,0,0,.7); }
.g span.k { background:linear-gradient(180deg,#F1D9A6,#C9A15F); -webkit-background-clip:text; background-clip:text; color:transparent; text-shadow:none; filter:drop-shadow(0 4px 18px rgba(201,161,95,.45)); }''',
    'chica-rosa': '''
.g { position:absolute; left:120px; right:120px; top:948px; text-align:center; opacity:0; }
.g span { display:inline-block; font-family:'Poppins',sans-serif; font-weight:600; font-size:64px; color:#fff; margin:0 6px; text-shadow:0 3px 12px rgba(0,0,0,.45); }
.g span.k { background:var(--acento2); color:var(--tinta); padding:2px 18px 6px; border-radius:18px; text-shadow:none; }''',
    'tutorial': '''
.g { position:absolute; left:120px; right:120px; top:978px; text-align:center; opacity:0; }
.g span { font-family:'Poppins',sans-serif; font-weight:700; font-size:66px; color:#fff; text-shadow:0 3px 14px rgba(0,0,0,.6); }
.g span.k { color:var(--acento); }''',
}

SUB_HTML = '''<!doctype html>
<html lang="es"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Poppins:wght@600;700;800&family=Playfair+Display:ital,wght@1,600&family=Inter:wght@700&display=block" />
<style>
:root {{ --acento:{acento}; --acento2:{acento2}; --tinta:{tinta}; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1080px; height:1920px; overflow:hidden; background:transparent; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; }}
{css}
.g span + span {{ margin-left: .26em; }}
#flash {{ position:absolute; inset:0; background:#fff; opacity:0; }}
#luz {{ position:absolute; inset:0; opacity:0; background:radial-gradient(70% 50% at 50% 30%, rgba(255,236,200,.5), transparent 70%); }}
#marca {{ position:absolute; left:50%; top:1500px; width:132px; margin-left:-66px; opacity:.95; filter:drop-shadow(0 2px 6px rgba(0,0,0,.45)); }}
</style></head><body>
<div id="root" data-composition-id="subs" data-start="0" data-duration="{dur:.3f}" data-width="1080" data-height="1920">
<div id="luz"></div><div id="flash"></div>{marca}
{grupos}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{anim}
tl.set({{}}, {{}}, {dur:.3f});
window.__timelines = window.__timelines || {{}};
window.__timelines["subs"] = tl;
</script></body></html>'''


def limpiar(t):
    return t.strip()


def agrupar(palabras, estilo, claves, ocultos):
    claves = {c.lower().strip('.,¿?¡!') for c in claves}
    maxp = 1 if estilo == 'impacto' else 2 if estilo in ('editorial', 'cinematico') else 3
    grupos, g = [], []
    for w in palabras:
        if any(a <= w['start'] < b for a, b in ocultos):
            continue
        limpio = w['text'].lower().strip('.,¿?¡!')
        es_clave = limpio in claves
        corte = g and (len(g) >= maxp or es_clave or any(x['clave'] for x in g) or w['start'] - g[-1]['end'] > .25
                       or sum(len(x['text']) for x in g) + len(w['text']) > 16 or g[-1]['text'][-1:] in '.,?!')
        if corte:
            grupos.append(g); g = []
        g.append(dict(w, clave=es_clave))
    if g:
        grupos.append(g)
    return grupos


def html_subs(palabras, estilo, plan, dur):
    col = plan.get('colores', {})
    ocultos = plan.get('_ocultos', [])
    grupos = agrupar(palabras, estilo, plan.get('claves', []), ocultos)
    divs, js = [], []
    for i, g in enumerate(grupos):
        a = g[0]['start']
        b = grupos[i + 1][0]['start'] if i + 1 < len(grupos) else g[-1]['end'] + .4
        b = min(b, g[-1]['end'] + .6)
        clave = any(x['clave'] for x in g)
        spans = ' '.join(f'<span class="{"k" if x["clave"] else ""}">{html.escape(x["text"].strip(".,") if estilo == "impacto" else x["text"])}</span>' for x in g)
        divs.append(f'<div class="g{" clave" if clave else ""}" id="g{i}">{spans}</div>')
        if estilo == 'impacto':
            js.append(f"tl.set('#g{i}',{{opacity:1}},{a:.3f}).fromTo('#g{i}',{{scale:{1.35 if clave else 1.15}}},{{scale:1,duration:.16,ease:'back.out(3)',immediateRender:false}},{a:.3f}).set('#g{i}',{{opacity:0}},{b:.3f});")
        else:
            js.append(f"tl.fromTo('#g{i}',{{opacity:0,y:24,filter:'blur(6px)'}},{{opacity:1,y:0,filter:'blur(0px)',duration:.18,ease:'power3.out',immediateRender:false}},{a:.3f}).set('#g{i}',{{opacity:0}},{b:.3f});")
    for z in plan.get('_zooms', []):
        if z.get('tipo') in ('flash', 'luz'):
            js.append(anim_zooms([z]))
    modo = plan.get('marca', 'final')   # 'final' (por defecto): solo en el cierre · 'siempre' · false
    marca = '<img id="marca" src="levelup-logo.png" />' if modo else ''
    if modo and modo != 'siempre':
        js.append("tl.set('#marca',{opacity:0},0);")
        for a, b in plan.get('_marca', []):
            js.append(f"tl.fromTo('#marca',{{opacity:0,scale:.7,y:16}},{{opacity:.95,scale:1,y:0,duration:.35,ease:'back.out(2)',immediateRender:false}},{a:.3f})"
                      f".to('#marca',{{opacity:0,duration:.25}},{max(a + .4, b - .25):.3f});")
    return SUB_HTML.format(css=SUB_CSS[estilo], grupos='\n'.join(divs), anim='\n'.join(js), dur=dur, marca=marca,
                           acento=col.get('acento', '#C9A15F'), acento2=col.get('acento2', '#E9D88C'), tinta=col.get('tinta', '#3A2A1F')), grupos


# ---------------------------------------------------------------- 4. motion graphics del banco
def catalogo():
    c = json.load(open(os.path.join(BANCO, 'catalogo.json')))
    return {m['id']: m for e in c['estilos'] for m in e['motion']}


def render_hf(dir_proyecto, salida, comp=None, variables=None, formato='mp4', borrador=False):
    cmd = ['npx', 'hyperframes', 'render', dir_proyecto, '-o', salida, '--format', formato, '-q', 'draft' if borrador else 'standard']
    if comp:
        cmd += ['-c', comp]
    if variables:
        cmd += ['--variables', json.dumps(variables, ensure_ascii=False)]
    sh(cmd, cwd=dir_proyecto)


def render_motion(m, variables, cache_dir, borrador):
    clave = hashlib.md5((m['archivo'] + json.dumps(variables, sort_keys=True) + str(os.path.getmtime(os.path.join(BANCO, m['archivo'])))).encode()).hexdigest()[:10]
    out = os.path.join(cache_dir, f"{m['id']}-{clave}.webm")
    if not os.path.exists(out):
        render_hf(BANCO, out, comp=m['archivo'], variables=variables, formato='webm', borrador=borrador)
    return out


# ---------------------------------------------------------------- 5. recorte de persona (efecto detrás)
def recorte(base, t, d, out):
    if os.path.exists(out):
        return out
    import cv2
    import numpy as np
    import mediapipe as mp
    tmp = out + '.frames'
    os.makedirs(tmp, exist_ok=True)
    cap = cv2.VideoCapture(base)
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
    seg = mp.solutions.selfie_segmentation.SelfieSegmentation(model_selection=0)
    n = int(round(d * FPS))
    prev = None
    for i in range(n):
        ok, f = cap.read()
        if not ok:
            break
        m = seg.process(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)).segmentation_mask
        m = cv2.GaussianBlur(m, (7, 7), 0)
        if prev is not None:
            m = .6 * m + .4 * prev
        prev = m
        a = np.clip((m - .35) / .3, 0, 1)
        rgba = np.dstack([f, (a * 255).astype('uint8')])
        cv2.imwrite(os.path.join(tmp, f'{i:05d}.png'), rgba)
    sh(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', os.path.join(tmp, '%05d.png'), '-c:v', 'libvpx-vp9', '-pix_fmt', 'yuva420p', '-b:v', '4M', '-auto-alt-ref', '0', out])
    subprocess.run(['rm', '-rf', tmp])
    return out


# ---------------------------------------------------------------- 5b. FreezeFrame (congelar)
def congelado(base, t, d, out_webm):
    """Toma el cuadro t de base.mp4 y arma una capa: fondo gris 40% más oscuro, tú a color 4% más grande,
    borde blanco de ~12 px detrás de ti y sombra suave. Se ve como sticker. Dura d s y se suelta en 1/3 s."""
    if os.path.exists(out_webm):
        return out_webm
    import cv2
    import numpy as np
    import mediapipe as mp
    cap = cv2.VideoCapture(base)
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
    ok, f = cap.read()
    seg = mp.solutions.selfie_segmentation.SelfieSegmentation(model_selection=0)
    m = seg.process(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)).segmentation_mask
    m = cv2.GaussianBlur(np.clip((m - .4) / .25, 0, 1).astype(np.float32), (5, 5), 0)
    h, w = m.shape
    ys, xs = np.where(m > .5)
    cx, cy = (int(xs.mean()), int(np.percentile(ys, 70))) if len(xs) else (w // 2, h // 2)
    M = cv2.getRotationMatrix2D((cx, cy), 0, 1.04)
    fg = cv2.warpAffine(f, M, (w, h)); mg = cv2.warpAffine(m, M, (w, h))
    borde = cv2.dilate((mg > .5).astype(np.uint8) * 255, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))).astype(np.float32) / 255
    borde = cv2.GaussianBlur(borde, (3, 3), 0)
    sombra = cv2.GaussianBlur(np.roll(borde, 18, axis=0), (0, 0), 14) * .45
    gris = cv2.cvtColor(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR).astype(np.float32) * .6
    img = gris * (1 - sombra[..., None])
    img = img * (1 - borde[..., None]) + 255 * borde[..., None]
    img = img * (1 - mg[..., None]) + fg.astype(np.float32) * mg[..., None]
    png = out_webm + '.png'
    cv2.imwrite(png, np.clip(img, 0, 255).astype(np.uint8))
    sh(['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-framerate', str(FPS), '-i', png, '-t', f'{d + 1 / 3:.3f}',
        '-vf', f'format=yuva420p,fade=t=out:st={d:.3f}:d=0.333:alpha=1', '-c:v', 'libvpx-vp9', '-pix_fmt', 'yuva420p', '-b:v', '6M', '-auto-alt-ref', '0', out_webm])
    os.remove(png)
    return out_webm


# ---------------------------------------------------------------- 6. montaje final
# Movimiento de cámara de Over The Shoulder (cuadros relativos al inicio; escala, x, y). Igual que la versión Remotion.
CAMARA_HOMBROS = [(0, 1, 0, 0), (5, 1, 0, 0), (20, 1.3, 155, 120), (27, 1.3, 147, 114), (36, 1.12, 0, 60),
                  (46, 1.3, -155, 120), (55, 1.3, -149, 116), (70, 1, 0, 0)]
TRAMOS_MOVIMIENTO = [(5, 20), (27, 36), (36, 46), (55, 70)]   # aquí la cámara se mueve → desenfoque


def expr_camara(inicios):
    """Expresiones ffmpeg S(t), X(t), Y(t) con suavizado ease-in-out en cada tramo."""
    E = lambda p: f'if(lt({p},0.5),4*pow({p},3),1-pow(-2*{p}+2,3)/2)'
    def campo(i, base):
        partes = []
        for t0 in inicios:
            for (fa, *va), (fb, *vb) in zip(CAMARA_HOMBROS, CAMARA_HOMBROS[1:]):
                a, b = t0 + fa / FPS, t0 + fb / FPS
                v0, v1 = va[i], vb[i]
                if v0 == base and v1 == base:
                    continue
                p = f'((t-{a:.4f})/{b - a:.4f})'
                partes.append(f'gte(t,{a:.4f})*lt(t,{b:.4f})*({v0 - base}+({v1 - v0})*{E(p)})')
        return f'{base}+' + '+'.join(partes) if partes else str(base)
    return campo(0, 1), campo(1, 0), campo(2, 0)


def montar(base, subs, capas, sonidos, out, dur, camaras=None):
    ins = ['-i', base]
    f = []
    actual = '[0:v]'
    k = 1
    for c in capas:  # capas = [(archivo, t, dur)] en orden de abajo a arriba
        ins += ['-c:v', 'libvpx-vp9', '-itsoffset', f'{c[1]:.3f}', '-i', c[0]]
        f.append(f'{actual}[{k}:v]overlay=0:0:eof_action=pass:enable=\'between(t,{c[1]:.3f},{c[1] + c[2]:.3f})\'[c{k}]')
        actual = f'[c{k}]'
        k += 1
    if camaras:   # la cámara mueve TODO (video + motion + tu recorte) pero no los subtítulos
        S_, X_, Y_ = expr_camara(camaras)
        it = lambda e: re.sub(r'\bt\b', 'it', e)
        cadena = f"{actual}zoompan=z='{it(S_)}':x='(iw-iw/zoom)/2-({it(X_)})/zoom':y='(ih-ih/zoom)/2-({it(Y_)})/zoom':d=1:s=1080x1920:fps=30"
        # desenfoque de movimiento direccional: más fuerte a mitad del tramo (donde va más rápido), nada en las pausas
        import math
        claves = {k[0]: k for k in CAMARA_HOMBROS}
        for t0 in camaras:
            for a, b in TRAMOS_MOVIMIENTO:
                (_, s0, x0, y0), (_, s1, x1, y1) = claves[a], claves[b]
                ang = math.degrees(math.atan2(y1 - y0, x1 - x0)) % 180 if (x1 - x0 or y1 - y0) else 90
                ta, tb = t0 + a / FPS, t0 + b / FPS
                m1, m2 = ta + (tb - ta) * .2, tb - (tb - ta) * .2
                cadena += f",dblur=angle={ang:.0f}:radius=5:enable='between(t,{ta:.3f},{tb:.3f})-between(t,{m1:.3f},{m2:.3f})'"
                cadena += f",dblur=angle={ang:.0f}:radius=14:enable='between(t,{m1:.3f},{m2:.3f})'"
        f.append(cadena + '[cam]')
        actual = '[cam]'
    ins += ['-c:v', 'libvpx-vp9', '-i', subs]
    f.append(f'{actual}[{k}:v]overlay=0:0:eof_action=pass,format=yuv420p[vout]')
    k += 1
    mezcla = ['[0:a]volume=1.0[voz]']
    etiquetas = ['[voz]']
    for i, s in enumerate(sonidos):
        ins += ['-i', s['archivo']]
        ms = int(max(0, s['t']) * 1000)
        mezcla.append(f'[{k}:a]volume={s.get("vol", .5)},adelay={ms}|{ms}[s{i}]')
        etiquetas.append(f'[s{i}]')
        k += 1
    mezcla.append(''.join(etiquetas) + f'amix=inputs={len(etiquetas)}:normalize=0:duration=first,alimiter=limit=0.95[aout]')
    sh(['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex', ';'.join(f + mezcla), '-map', '[vout]', '-map', '[aout]',
        '-t', f'{dur:.3f}', '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
        '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-c:a', 'aac', '-b:a', '192k', out])


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    plan_path = os.path.abspath(sys.argv[1])
    borrador = '--borrador' in sys.argv
    plan = json.load(open(plan_path))
    carpeta = os.path.dirname(plan_path)
    nombre = plan['nombre']
    estilo = plan['estilo']
    os.makedirs(os.path.join(carpeta, 'media'), exist_ok=True)
    os.makedirs(os.path.join(carpeta, 'capas'), exist_ok=True)
    palabras = json.load(open(os.path.join(RAIZ, plan['palabras'])))['words']

    print('1 · cortes, zooms y color…')
    piezas, mapa, pal, dur = preparar_palabras(plan, palabras)
    json.dump({'words': pal}, open(os.path.join(carpeta, 'palabras-cortadas.json'), 'w'), ensure_ascii=False, indent=0)
    T = lambda x: a_cortado(mapa, x)
    zooms = [dict(z, t=T(z['t'])) for z in plan.get('zooms', [])]
    plan['_zooms'] = zooms
    base = os.path.join(carpeta, 'capas', 'base.mp4')
    src = os.path.join(RAIZ, plan['video'])
    if any(z.get('tipo') in ('marco', 'dividida') for z in zooms):
        cortado = os.path.join(carpeta, 'media', 'cortado.mp4')
        cortar_video(src, piezas, cortado)
        subprocess.run(['cp', os.path.join(BANCO, 'assets', 'levelup-logo.png'), carpeta])
        open(os.path.join(carpeta, 'index.html'), 'w').write(BASE_HTML.format(dur=duracion(cortado), anim=anim_zooms(zooms), marca='', papel=plan.get('colores', {}).get('papel', '#F3ECE0')))
        render_hf(carpeta, base, borrador=borrador)
    else:
        base_ffmpeg(src, piezas, zooms, base, color=plan.get('color', True))
    ocultos_fx, marca_fx = [], []
    if plan.get('camara_fx'):   # 51 efectos de cámara (fx-camara/ · Level Up): siguen tu cara y van detrás de ti
        print('2 · efectos de cámara…')
        fxp = os.path.join(carpeta, 'capas', 'camara-fx.json')
        ocultos_fx = []
        lista = []
        for e in plan['camara_fx']:
            e = dict(e); t0 = T(e.pop('t')); d = e.pop('dur', 2.5)
            if 'ticks' in e:   # segundos del video original → editado (todo: absolutos; apple-toggles: desde el inicio del efecto)
                rel = 0 if e['fx'] == 'todo' else t0
                e['ticks'] = '|'.join(f"{T(float(x)) - rel:.2f}" for x in str(e['ticks']).split('|'))
            if e.pop('ocultar_subs', e['fx'] in BAJO_BARBILLA and e.get('pos', 'below' if e['fx'] != 'apple-toggles' else 'above') == 'below'):
                ocultos_fx.append((t0, t0 + d))
            if 'at' in e: e['at'] = round(T(float(e['at'])), 2)
            lista.append(dict(e, start=round(t0, 3), end=round(t0 + d, 3)))
            if e['fx'] in CTA_FX: marca_fx.append((t0, t0 + d))
            print(f"   {e['fx']} en {t0:.1f}s")
        json.dump({'effects': lista}, open(fxp, 'w'), ensure_ascii=False, indent=1)
        con_fx = os.path.join(carpeta, 'capas', 'base-fx.mp4')
        subprocess.run([sys.executable, os.path.join(RAIZ, 'fx-camara', 'scripts', 'fx.py'), '--plan', fxp, base, con_fx], check=True)
        base = con_fx
    dur = duracion(base)
    print(f'   {len(piezas)} piezas · {dur:.1f} s')
    if '--solo-base' in sys.argv:
        return

    print('3 · motion graphics…')
    cat = catalogo()
    capas, sonidos, ocultos = [], [], list(ocultos_fx)
    efectos = json.load(open(os.path.join(SONIDOS, 'sonidos.json')))
    trans = efectos['transiciones']
    for i, it in enumerate(plan.get('motions', [])):
        m = cat[it['id']]
        t = T(it['t'])
        d = it.get('dur', m['dur'])
        v = dict(it.get('vars', {}))
        v.setdefault('fondo', 'transparente' if m['tipo'] == 'encima' else 'hoja')
        v.update({k: c for k, c in plan.get('colores', {}).items() if k not in v})
        arch = render_motion(m, v, os.path.join(carpeta, 'capas'), borrador)
        capas.append((arch, t, d))
        if it.get('detras'):
            capas.append((recorte(base, t, d, os.path.join(carpeta, 'capas', f'persona-{i}.webm')), t, d))
        if it.get('ocultar_subs') or m['tipo'] == 'pantalla' or v.get('fondo') == 'hoja':
            ocultos.append((t, t + d))
        for s in (it.get('sfx', m.get('sfx', [])) if plan.get('efectos_sonido') else []):
            sonidos.append(dict(archivo=os.path.join(SONIDOS, efectos['efectos'][s['s']]['archivo']), t=t + s.get('en', 0), vol=s.get('vol', .45)))
        print(f"   {m['id']} en {t:.1f}s")
    for i, z in enumerate(zooms):
        if z.get('tipo') == 'congelar':   # FreezeFrame: imagen congelada tipo sticker (la etiqueta y el flash van con el motion cl05)
            d = z.get('dur', 1.5)
            capas.insert(0, (congelado(base, z['t'], d, os.path.join(carpeta, 'capas', f'congelado-{i}.webm')), z['t'], d + 1 / 3))  # debajo de los motion
            print(f"   congelar en {z['t']:.1f}s")
    con_sonido = plan.get('efectos_sonido', False) and trans
    for j, s in enumerate(plan.get('sonidos', []) if con_sonido else []):
        if s['s'] == 'whoosh':
            tr = trans[(s.get('n', j * 7)) % len(trans)]
            sonidos.append(dict(archivo=os.path.join(SONIDOS, tr['archivo']), t=T(s['t']) - tr['golpe'], vol=s.get('vol', .35)))
        else:
            sonidos.append(dict(archivo=os.path.join(SONIDOS, efectos['efectos'][s['s']]['archivo']), t=T(s['t']), vol=s.get('vol', .45)))
    for z in zooms:
        if con_sonido and z.get('tipo', 'golpe') == 'golpe' and z.get('whoosh', True):
            tr = trans[int(z['t'] * 13) % len(trans)]
            sonidos.append(dict(archivo=os.path.join(SONIDOS, tr['archivo']), t=z['t'] - tr['golpe'], vol=.28))

    if not plan.get('efectos_sonido', False):
        sonidos = []   # sin efectos de sonido (solo tu voz) hasta tener el pack nuevo
    marca_v = list(marca_fx) + [(T(it['t']), T(it['t']) + it.get('dur', cat[it['id']]['dur'])) for it in plan.get('motions', []) if it['id'] in CTA_MOTION]
    juntas = []
    for a, b in sorted(marca_v + [(max(0, dur - 2.5), dur)]):   # logo: solo en el cierre/CTA y los últimos 2,5 s
        if juntas and a <= juntas[-1][1] + .3: juntas[-1] = (juntas[-1][0], max(b, juntas[-1][1]))
        else: juntas.append((a, b))
    plan['_marca'] = juntas
    print('4 · subtítulos…')
    plan['_ocultos'] = ocultos
    shtml, grupos = html_subs(pal, estilo, plan, dur)
    if plan.get('clic_subs') and plan.get('efectos_sonido', False):
        desde = T(plan['clic_subs'])
        for g in grupos:
            if g[0]['start'] >= desde and any(x['clave'] for x in g):
                sonidos.append(dict(archivo=os.path.join(SONIDOS, 'clic-suave.mp3'), t=g[0]['start'], vol=.35))
    sub_dir = os.path.join(carpeta, 'subs')
    os.makedirs(sub_dir, exist_ok=True)
    subprocess.run(['cp', os.path.join(BANCO, 'assets', 'levelup-logo.png'), sub_dir])
    open(os.path.join(sub_dir, 'index.html'), 'w').write(shtml)
    subs = os.path.join(carpeta, 'capas', 'subtitulos.webm')
    render_hf(sub_dir, subs, formato='webm', borrador=borrador)

    print('5 · montaje final…')
    os.makedirs(os.path.join(RAIZ, 'out'), exist_ok=True)
    out = os.path.join(RAIZ, 'out', f'{nombre}{"-borrador" if borrador else ""}.mp4')
    camaras = [T(it['t']) for it in plan.get('motions', []) if it.get('camara')]
    montar(base, subs, capas, sonidos, out, dur, camaras)
    print(f'✓ {out}  ({dur:.1f} s)')


if __name__ == '__main__':
    main()
