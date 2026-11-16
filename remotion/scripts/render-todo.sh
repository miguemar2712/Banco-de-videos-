#!/bin/sh
# Renderiza cada efecto a out/<Efecto>.mp4 y el reel completo a out/full-reel.mp4
cd "$(dirname "$0")/.."
for c in OverTheShoulder GlassGraph FreezeFrame TierList TextBehind ColorGrade ChatRender; do
  npx remotion render src/index.ts $c out/$c.mp4 --codec=h264 --crf=16 --log=error >/dev/null 2>&1 && echo "✓ out/$c.mp4" || echo "FALLÓ $c"
done
npx remotion render src/index.ts FullReel out/full-reel.mp4 --codec=h264 --crf=16 --log=error >/dev/null 2>&1 && echo "✓ out/full-reel.mp4" || echo "FALLÓ FullReel"
