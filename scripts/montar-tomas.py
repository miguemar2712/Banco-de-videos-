#!/usr/bin/env python3
"""Monta un video SOLO de tomas al ritmo de una voz en off (sin subtítulos).

uso:  .venv/bin/python scripts/montar-tomas.py ediciones/<nombre>/tomas.json
      .venv/bin/python scripts/montar-tomas.py --descargar      (baja todo el banco de b-roll de broll/catalogo.json)

tomas.json:
{
  "voz": "videos/voz-x.m4a",
  "salida": "out/x.mp4",
  "tomas": [                                   # una detrás de otra; "hasta" = segundo de la voz donde termina la toma
    {"hasta": 3.5, "clip": "videos/clip-b.mp4", "desde": 2.0},
    {"hasta": 5.9, "clip": "broll:dinero"},    # toma del banco (broll/catalogo.json); rota para no repetir
    {"hasta": 7.3, "clip": "broll:china", "recorte": 0.3}   # recorte: 0 = izquierda · 0.5 = centro · 1 = derecha
  ],
  "textos": [                                  # opcional: SOLO textos puntuales que la persona pida
    {"de": 4.95, "a": 5.95, "grande": "$15", "cursiva": "dólares", "cursiva_de": 5.40}
  ]
}
"""
import json, os, subprocess, sys

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CAT = os.path.join(RAIZ, 'broll', 'catalogo.json')
BROLL = os.path.join(RAIZ, 'videos', 'broll')
FUENTES = os.path.join(RAIZ, 'fx-camara', 'fonts')


def sh(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def info(p):
    w, h, d = sh(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height:format=duration',
                  '-of', 'csv=p=0:s=,', p]).replace('\n', ',').strip(',').split(',')[:3]
    return int(w), int(h), float(d)


def archivo_broll(i):
    return os.path.join(BROLL, f"mk-{i}.mp4")


def descargar(ids):
    os.makedirs(BROLL, exist_ok=True)
    for i in ids:
        dst = archivo_broll(i)
        if os.path.exists(dst) and os.path.getsize(dst) > 0:
            continue
        for r in (1080, 720):
            if subprocess.run(['curl', '-sSf', f'https://assets.mixkit.co/videos/{i}/{i}-{r}.mp4', '-o', dst]).returncode == 0:
                print('↓', i, r); break
        else:
            print('✗ no se pudo bajar', i)


# ---------------------------------------------------------------- título + subtítulos estilo CapCut (gusto de @delcarmen__1)
#  Título fijo arriba en Montserrat Black blanca con sombra; subtítulos en MAYÚSCULAS Montserrat ExtraBold que aparecen
#  palabra por palabra, escalonados (una palabra por línea, alternando izquierda/derecha); las claves, más grandes.
ASS_CAB = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Titulo,Montserrat Black,128,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1
Style: Sombra,Montserrat Black,128,&H70000000,&H70000000,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1
Style: Sub,Montserrat ExtraBold,64,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,0,0,4,0,0,0,1
Style: SubSombra,Montserrat ExtraBold,64,&H80000000,&H80000000,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,0,0,4,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def tc(s):
    s = max(0, s); h = int(s // 3600); m = int(s % 3600 // 60)
    return f"{h}:{m:02d}:{s % 60:05.2f}"


def doble(capa, a, b, estilo, x, y, txt, tags='', sombra=(5, 8), blur=6):
    """Texto blanco + su sombra difuminada debajo (como CapCut)."""
    sx, sy = sombra
    return (f"Dialogue: {capa},{tc(a)},{tc(b)},{estilo.replace('Sub', 'SubSombra') if estilo.startswith('Sub') else 'Sombra'},,0,0,0,,"
            f"{{\\pos({x + sx},{y + sy})\\blur{blur}{tags}}}{txt}\n"
            f"Dialogue: {capa + 1},{tc(a)},{tc(b)},{estilo},,0,0,0,,{{\\pos({x},{y}){tags}}}{txt}\n")


def hacer_ass(plan, total):
    out = ASS_CAB
    t = plan.get('titulo')
    if t:
        lineas = [t] if isinstance(t, str) else t
        y0 = plan.get('titulo_y', 290)
        for i, l in enumerate(lineas):
            fs = min(170, int(960 / (len(l) * .56)))
            out += doble(0, 0, total, 'Titulo', 540, y0 + i * int(fs * .9), l.upper(), f'\\fs{fs}', sombra=(7, 10), blur=8)
    if plan.get('subtitulos'):
        ws = json.load(open(os.path.join(RAIZ, plan['palabras'])))['words']
        rep = {k.lower(): v for k, v in plan.get('reemplazos', {}).items()}
        claves = {c.lower() for c in plan.get('claves', [])}
        pal = []
        for w in ws:
            base = w['text'].strip().strip('.,¿?¡!')
            nuevo = rep.get(base.lower(), base)
            for i, p in enumerate(nuevo.split()):
                pal.append(dict(t=p.upper(), a=w['start'], b=w['end'], clave=base.lower() in claves,
                                fin=(i == len(nuevo.split()) - 1) and w['text'].strip()[-1:] in '.,?!'))
        grupos, g = [], []
        for w in pal:
            if g and (len(g) >= 3 or w['a'] - g[-1]['b'] > .3 or g[-1]['fin'] or w['clave'] != g[-1]['clave']):
                grupos.append(g); g = []
            g.append(w)
        grupos.append(g)
        Y = plan.get('subs_y', 1180)
        for k, g in enumerate(grupos):
            fin = min(grupos[k + 1][0]['a'] if k + 1 < len(grupos) else g[-1]['b'] + .5, g[-1]['b'] + .7)
            grande = g[0]['clave']
            for j, w in enumerate(g):
                if grande:   # palabra clave: grande y centrada, una debajo de otra
                    tam = min(140, int(900 / (len(w['t']) * .72)))
                    x, y, al = 540, Y + j * int(tam * .95), '\\an5'
                else:        # palabras normales: escalonadas izquierda/derecha
                    tam = 98
                    x, y, al = 270 + (180 if j % 2 else 0), Y + j * 88, '\\an4'
                pop = f"{al}\\fs{tam}\\fscx125\\fscy125\\t(0,90,\\fscx100\\fscy100)"
                out += doble(2, w['a'], fin, 'Sub', x, y, w['t'], pop, sombra=(5, 7), blur=6)
    return out


def main():
    cat = json.load(open(CAT)) if os.path.exists(CAT) else {'categorias': {}}
    if '--descargar' in sys.argv:
        descargar([t['id'] for c in cat['categorias'].values() for t in c['tomas']])
        return
    plan = json.load(open(sys.argv[1]))
    uso = {}
    entradas, partes, prev = [], [], 0.0
    for k, t in enumerate(plan['tomas']):
        dur = round(t['hasta'] - prev, 3); prev = t['hasta']
        clip, desde, rec = t['clip'], t.get('desde'), t.get('recorte')
        if clip.startswith('broll:'):
            c = clip.split(':', 1)[1]
            lista = cat['categorias'][c]['tomas']
            n = uso.get(c, 0); uso[c] = n + 1
            elegido = next((x for x in lista if str(x['id']) == str(t['id'])), None) if t.get('id') else lista[n % len(lista)]
            descargar([elegido['id']])
            clip = archivo_broll(elegido['id'])
            desde = elegido.get('desde', 1.0) if desde is None else desde
            rec = elegido.get('recorte', 0.5) if rec is None else rec
        clip = os.path.join(RAIZ, clip) if not os.path.isabs(clip) else clip
        desde = desde or 0.0
        rec = 0.5 if rec is None else rec
        w, h, d = info(clip)
        if desde + dur > d:   # si el clip es corto, se ralentiza un poco para llenar
            vel = max(.5, (d - desde) / dur)
        else:
            vel = 1.0
        if w / h > 9 / 16 + .01:
            enc = f"crop=ih*9/16:ih:(iw-ow)*{rec}:0"
        else:
            enc = f"crop=iw:iw*16/9:0:(ih-oh)*{rec}"
        entradas += ['-i', clip]
        partes.append(f"[{k}:v]trim=start={desde:.3f}:duration={dur * vel:.3f},setpts=(PTS-STARTPTS)/{vel:.3f},"
                      f"{enc},scale=1080:1920:flags=lanczos,setsar=1,fps=30[s{k}]")
    nv = len(plan['tomas'])
    total = plan['tomas'][-1]['hasta']
    cadena = ''.join(f'[s{k}]' for k in range(nv)) + f'concat=n={nv}:v=1:a=0,format=yuv420p'
    for x in plan.get('textos', []):
        a, b = x['de'], x['a']
        def dt(txt, fuente, size, y, t0, lado):
            txt = txt.replace('\\', '\\\\').replace("'", "’").replace(':', '\\:').replace('%', '\\%')
            return (f",drawtext=fontfile={FUENTES}/{fuente}:text='{txt}':fontsize={size}:fontcolor=white:shadowcolor=black@0.45:"
                    f"shadowx=0:shadowy=7:x='(w-tw)/2{lado}360*pow(max(0\\,1-(t-{t0})/0.3)\\,3)':y={y}:"
                    f"alpha='min(1\\,max(0\\,(t-{t0})/0.12))':enable='between(t,{t0},{b})'")
        if x.get('grande'):
            cadena += dt(x['grande'], 'ArchivoBlack-Regular.ttf', x.get('tam', 300 if len(x['grande']) <= 5 else 170), x.get('y', 640), a, '-')
        if x.get('cursiva'):
            cadena += dt(x['cursiva'], 'PlayfairDisplay-Italic.ttf', 170, x.get('y', 640) + 325, x.get('cursiva_de', a + .3), '+')
    extra = []
    if plan.get('mapa'):            # mapa de China rojo con estrellas detrás del título
        extra += ['-i', os.path.join(RAIZ, 'assets', 'china-mapa.png')]
        cadena += f"[vb];[vb][{nv + 1}:v]overlay=x=(W-w)/2:y={plan.get('mapa_y', 60)}"
    if plan.get('titulo') or plan.get('subtitulos'):
        ass = os.path.join(RAIZ, os.path.dirname(sys.argv[1]), 'subs.ass')
        open(ass, 'w').write(hacer_ass(plan, total))
        cadena += f",subtitles=filename='{ass}':fontsdir='{os.path.join(RAIZ, 'fuentes')}'"
    filtro = ';'.join(partes) + ';' + cadena + '[v];' + f'[{nv}:a]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]'
    salida = os.path.join(RAIZ, plan['salida'])
    os.makedirs(os.path.dirname(salida), exist_ok=True)
    sh(['ffmpeg', '-v', 'error', '-y', *entradas, '-i', os.path.join(RAIZ, plan['voz']), *extra, '-filter_complex', filtro,
        '-map', '[v]', '-map', '[a]', '-t', f'{total:.3f}', '-c:v', 'libx264', '-crf', '16', '-preset', 'medium',
        '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
        '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', salida])
    print('✓', plan['salida'], f'({total:.1f} s)')


if __name__ == '__main__':
    main()
