#!/bin/sh
# uso: scripts/stills.sh Composicion "f1 f2 f3"  → out/stills/Composicion-fN.png
cd "$(dirname "$0")/.."
for f in $2; do
  npx remotion still src/index.ts "$1" "out/stills/$1-f$f.png" --frame=$f --log=error >/dev/null 2>&1 || echo "falló $1 $f"
done
