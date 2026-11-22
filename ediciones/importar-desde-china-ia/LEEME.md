Su video ya editado (con título "IMPORTAR DESDE CHINA??" sobre el mapa, sin subtítulos) + 3 tomas de b-roll nuevas
en su mismo tiempo (4.3–6.0 proveedores caminando 23237 · 6.0–7.6 contenedores 26950 · 7.6–9.7 billetes 18305 · 17.4–19.6 avión 6938).
Durante las tomas nuevas se pone encima titulo-mapa.png (réplica de su título) para que no desaparezca:
  .venv/bin/python scripts/montar-tomas.py ediciones/importar-desde-china-ia/tomas.json   (sale sin-titulo.mp4)
  ffmpeg -i ediciones/importar-desde-china-ia/sin-titulo.mp4 -loop 1 -i ediciones/importar-desde-china-ia/titulo-mapa.png \
    -filter_complex "[0:v][1:v]overlay=0:0:shortest=1:enable='between(t,4.3,9.7)+between(t,17.4,19.6)',format=yuv420p[v]" \
    -map "[v]" -map 0:a -c:v libx264 -crf 16 -c:a copy out/importar-desde-china-ia.mp4
