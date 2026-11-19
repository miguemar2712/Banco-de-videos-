#!/usr/bin/env python3
"""Copia la colección de @delcarmen__1 (coleccion/) a videos/ con sus alias y genera las versiones limpias 1080x1920
que usan los planes de ediciones/. Seguro de correr varias veces."""
import json, os, shutil, subprocess
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(RAIZ); os.makedirs('videos', exist_ok=True)
inv = json.load(open('coleccion/inventario.json'))
for f, x in inv.items():
    if not os.path.exists(x['alias']):
        shutil.copy(os.path.join('coleccion', f), x['alias']); print('→', x['alias'])
E = 'scale=1080:1920:flags=lanczos,format=yuv420p'
VERT = 'crop=ih*9/16:ih,' + E
limpias = {   # salida: (entrada, filtro, duración máx.)
 'videos/clip-a-1080.mp4': ('videos/clip-a.mov', E, None),
 'videos/clip-b-limpio.mp4': ('videos/clip-b.mov', 'delogo=x=165:y=472:w=250:h=88,' + E, None),
 'videos/clip-e-limpio.mp4': ('videos/clip-e.mov', "delogo=x=205:y=33:w=165:h=152:enable='between(t,0,3.95)+between(t,10.9,13.5)'," + E, 13.4),
 'videos/clip-f-1080.mp4': ('videos/clip-f.mov', E, None),
 'videos/clip-g-limpio.mp4': ('videos/clip-g.mov', 'delogo=x=135:y=465:w=310:h=110,' + E, None),
 'videos/clip-h-1080.mp4': ('videos/clip-h.mp4', E, None),
 'videos/clip-i-1080.mp4': ('videos/clip-i.mov', VERT, None),
 'videos/clip-j-1080.mp4': ('videos/clip-j.mov', E, None),
 'videos/clip-k-limpio.mp4': ('videos/clip-k.mov', 'crop=414:736:150:544,scale=1080:1920:flags=lanczos,unsharp=5:5:0.6,format=yuv420p', 4.15),  # sin letras
 'videos/clip-l-1080.mp4': ('videos/clip-l.mov', E, None),
 'videos/clip-n-1080.mp4': ('videos/clip-n.mov', E, None),
 'videos/clip-n-ajustado.mp4': ('videos/clip-n.mov', 'setpts=PTS/1.1376,fps=30,' + E, None),   # acelerado para el audio voz-7 (ediciones/puerta-de-tu-casa)
}
for out, (src, vf, dur) in limpias.items():
    if os.path.exists(out) or not os.path.exists(src): continue
    cmd = ['ffmpeg', '-v', 'error', '-y', '-i', src] + (['-t', str(dur)] if dur else []) + ['-vf', vf, '-an', '-c:v', 'libx264', '-crf', '15', out]
    subprocess.run(cmd, check=True); print('✓', out)
print('LISTO')
