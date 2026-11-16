#!/usr/bin/env bash
# Level Up · instalación (se puede correr varias veces). Termina con LISTO.
cd "$(dirname "$0")"
falta=0
command -v node >/dev/null 2>&1 || { echo "NECESITO_NODE: Mac: brew install node · Windows: winget install OpenJS.NodeJS.LTS"; falta=1; }
command -v ffmpeg >/dev/null 2>&1 || { echo "NECESITO_FFMPEG: Mac: brew install ffmpeg · Windows: winget install ffmpeg"; falta=1; }
PY=""
for v in python3.12 python3.11 python3.13 python3; do
  if command -v "$v" >/dev/null 2>&1 && "$v" -c 'import sys; sys.exit(0 if (3,10) <= sys.version_info[:2] <= (3,12) else 1)' 2>/dev/null; then PY="$v"; break; fi
done
[ -z "$PY" ] && { echo "NECESITO_PYTHON: Python 3.10–3.12 (Mac: brew install python@3.12 · Windows: winget install Python.Python.3.12)"; falta=1; }
[ $falta = 1 ] && exit 1

# entorno de Python propio de Level Up
if [ ! -x .venv/bin/python ]; then "$PY" -m venv .venv; fi
.venv/bin/python -m pip install -q --upgrade pip
.venv/bin/python -m pip install -q -r requirements.txt || exit 1
.venv/bin/python -c "import mediapipe, cv2, PIL, numpy, faster_whisper" || exit 1

# HyperFrames (motion graphics) se descarga solo con npx la primera vez
(cd banco && npx --yes hyperframes@0.9.34 --version >/dev/null 2>&1) || echo "AVISO: HyperFrames se descargará en el primer render"
mkdir -p videos ediciones out
echo "Usa .venv/bin/python para los scripts (o activa: source .venv/bin/activate)"
echo LISTO
