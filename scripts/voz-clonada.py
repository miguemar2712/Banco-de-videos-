#!/usr/bin/env python3
"""Genera voz en español con la voz de la creadora (Chatterbox multilingüe, licencia MIT).

uso: .venv-voz/bin/python scripts/voz-clonada.py voz/muestra.wav "texto" salida.wav [--exag 0.5] [--cfg 0.5]
Cada frase se genera por separado y se une con una pausa corta (suena más natural).
"""
import re, sys
import torch, torchaudio as ta
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

args = [a for a in sys.argv[1:] if not a.startswith('--')]
opt = lambda k, d: float(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else d
ref, texto, out = args[0], args[1], args[2]
exag, cfg = opt('--exag', 0.5), opt('--cfg', 0.5)

torch.manual_seed(int(opt('--seed', 7)))
m = ChatterboxMultilingualTTS.from_pretrained(device='cpu')
frases = [f.strip() for f in re.split(r'(?<=[.?!])\s+', texto) if f.strip()]
partes = []
for f in frases:
    print('·', f, flush=True)
    wav = m.generate(f, language_id='es', audio_prompt_path=ref, exaggeration=exag, cfg_weight=cfg)
    partes += [wav, torch.zeros(1, int(m.sr * 0.18))]
ta.save(out, torch.cat(partes[:-1], dim=1), m.sr)
print('✓', out)
