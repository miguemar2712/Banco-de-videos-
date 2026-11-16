#!/bin/sh
# Prepara los videos del iPhone para editar:
#  1) Conversión HDR → SDR con el motor de Apple (avconvert, el mismo de Fotos): color natural, sin lavado.
#  2) Transcripción por palabra con Whisper.
# Uso: scripts/preparar-videos.sh "video1.mov" "video2.mov" ...
#      → videos/v1-apple.mov + videos/v1-palabras.json, v2…
cd "$(dirname "$0")/.."
mkdir -p videos
i=${INICIO:-1}
for src in "$@"; do
  out="videos/v$i-apple.mov"
  echo "== $src → $out"
  avconvert -s "$src" -p PresetHighestQuality -o "$out" --replace >/dev/null 2>&1 || {
    echo "   avconvert no disponible, uso ffmpeg"; ffmpeg -v error -y -i "$src" -vf "scale=1080:1920:in_color_matrix=bt2020:out_color_matrix=bt709,format=yuv420p" -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:v libx264 -crf 14 -c:a aac -b:a 256k "videos/v$i-apple.mp4"; out="videos/v$i-apple.mp4"; }
  PY=python3; [ -x .venv/bin/python ] && PY=.venv/bin/python
  $PY scripts/transcribir.py "$out" "videos/v$i-palabras.json" medium
  i=$((i+1))
done
echo LISTO
