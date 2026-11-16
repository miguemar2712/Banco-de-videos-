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
    filtro = ';'.join(partes) + ';' + cadena + '[v];' + f'[{nv}:a]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]'
    salida = os.path.join(RAIZ, plan['salida'])
    os.makedirs(os.path.dirname(salida), exist_ok=True)
    sh(['ffmpeg', '-v', 'error', '-y', *entradas, '-i', os.path.join(RAIZ, plan['voz']), '-filter_complex', filtro,
        '-map', '[v]', '-map', '[a]', '-t', f'{total:.3f}', '-c:v', 'libx264', '-crf', '16', '-preset', 'medium',
        '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
        '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', salida])
    print('✓', plan['salida'], f'({total:.1f} s)')


if __name__ == '__main__':
    main()
